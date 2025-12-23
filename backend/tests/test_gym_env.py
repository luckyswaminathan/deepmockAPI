import httpx
import pytest

from rl.gym_env import DeepMockGymEnv


def _build_transport(actions, obs_initial, obs_after, counts):
    primary_action_id = actions[0].get("action_id") or "POST:/v1/customers"

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/rl/goals":
            return httpx.Response(
                200,
                json={
                    "goal_id": "goal_test",
                    "api_slug": "stripe",
                    "description": "create customer",
                    "start_state_id": "state_seed",
                    "goal_state": {"target_components": {"customer": [{}]}},
                    "reward_config": None,
                },
            )
        if request.url.path == "/rl/goals/goal_test/episodes":
            return httpx.Response(
                200,
                json={
                    "episode_id": "episode_1",
                    "goal_id": "goal_test",
                    "current_state_id": "state_seed",
                    "action_history": [],
                    "reward": 0.0,
                    "done": False,
                    "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-01-01T00:00:00Z",
                },
            )
        if request.url.path == "/rl/episodes/episode_1/observation":
            counts["observation"] += 1
            payload = obs_initial if counts["observation"] == 1 else obs_after
            return httpx.Response(200, json=payload)
        if request.url.path == "/rl/episodes/episode_1/valid-actions":
            counts["valid"] += 1
            return httpx.Response(
                200,
                json={
                    "state_id": "state_seed",
                    "valid_action_ids": [primary_action_id],
                    "total_actions": len(actions),
                },
            )
        if request.url.path == "/rl/episodes/episode_1/actions":
            counts["actions"] += 1
            return httpx.Response(
                200,
                json={
                    "action_id": "action_001",
                    "next_state_id": "state_next",
                    "reward": 0.5,
                    "done": False,
                    "reason": "ok",
                    "response_status": 200,
                    "response_body": {"id": "cus_123"},
                },
            )
        return httpx.Response(404, json={"detail": "not found", "path": str(request.url)})

    return httpx.MockTransport(handler)


def test_gym_env_reset_and_step_with_masking():
    actions = [
        {"method": "POST", "path": "/v1/customers"},
        {"method": "GET", "path": "/v1/customers/{id}"},
    ]
    obs_initial = {
        "required": ["customer"],
        "satisfied": [],
        "known_ids": {},
        "last_k_components": [],
        "last_action_id": None,
        "last_status": None,
        "steps_remaining": 2,
    }
    obs_after = {
        "required": ["customer"],
        "satisfied": ["customer"],
        "known_ids": {"customer": ["cus_123"]},
        "last_k_components": ["customer"],
        "last_action_id": "action_001",
        "last_status": 200,
        "steps_remaining": 1,
    }
    counts = {"observation": 0, "valid": 0, "actions": 0}

    transport = _build_transport(actions, obs_initial, obs_after, counts)
    client = httpx.Client(transport=transport, base_url="http://testserver")

    env = DeepMockGymEnv(
        backend_url="http://testserver",
        api_slug="stripe",
        goal={"goal_state": {"target_components": {"customer": [{}]}}, "description": "create customer"},
        actions=actions,
        client=client,
        max_steps=5,
    )

    try:
        obs, info = env.reset()
        assert obs["required"] == ["customer"]
        assert info["episode_id"] == "episode_1"
        assert counts["observation"] == 1

        obs_next, reward, terminated, truncated, info_step = env.step(0)
        assert reward == pytest.approx(0.5)
        assert terminated is False
        assert truncated is False
        assert obs_next["satisfied"] == ["customer"]
        assert counts["actions"] == 1
        assert counts["valid"] == 1  # action mask consulted

        # Second action is invalid per mask; it should not hit the backend
        obs_invalid, penalty, term2, trunc2, info_invalid = env.step(1)
        assert info_invalid.get("invalid_action") is True
        assert penalty == pytest.approx(env.invalid_action_penalty)
        assert term2 is False
        assert trunc2 is False
        assert counts["actions"] == 1  # unchanged
        assert obs_invalid == obs_next  # state did not change
    finally:
        env.close()
