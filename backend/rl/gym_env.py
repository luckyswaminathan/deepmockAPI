"""Gym-compatible wrapper around the DeepMock RL endpoints."""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

import httpx
import numpy as np

try:  # Prefer gymnasium but gracefully fall back to classic gym
    import gymnasium as gym  # type: ignore
    from gymnasium import spaces  # type: ignore
    _GYM_AVAILABLE = True
except ImportError:  # pragma: no cover - only used if gymnasium is unavailable
    try:
        import gym  # type: ignore
        from gym import spaces  # type: ignore
        _GYM_AVAILABLE = True
    except ImportError:  # pragma: no cover - neither gym nor gymnasium installed
        gym = None  # type: ignore
        spaces = None  # type: ignore
        _GYM_AVAILABLE = False


def _normalize_path(api_slug: str, path: str) -> str:
    """Normalize an API path to the form expected by RL routes."""
    normalized = path.strip() or "/"
    if not normalized.startswith("/"):
        normalized = f"/{normalized}"

    prefix = f"/generated/{api_slug}"
    if normalized.startswith(prefix):
        normalized = normalized[len(prefix) :] or "/"
    return normalized


def _component_from_path(path: str) -> Optional[str]:
    """Heuristic to derive a component/resource name from a route."""
    parts = [p for p in path.strip("/").split("/") if p and not p.startswith("{")]
    if not parts:
        return None
    resource = parts[-1]
    if resource.endswith("ies"):
        component = resource[:-3] + "y"
    elif resource.endswith("s") and len(resource) > 1:
        component = resource[:-1]
    else:
        component = resource
    return component.replace("-", "_").lower()


class DeepMockGymEnv(gym.Env):
    """Gym-compatible environment that proxies DeepMock's RL endpoints.

    The environment wraps the /rl API surface:
    - reset(): creates (or reuses) a goal and starts an episode
    - step(): executes an action via /rl/episodes/{episode_id}/actions
    - observations: pulled from /rl/episodes/{episode_id}/observation

    By default, the action space is a Discrete over discovered OpenAPI routes,
    and observations follow the RL observation schema.
    """

    metadata = {"render_modes": ["human"]}

    def __init__(
        self,
        *,
        backend_url: str,
        api_slug: str,
        goal: Optional[Dict[str, Any]] = None,
        goal_id: Optional[str] = None,
        actions: Optional[Sequence[Dict[str, Any]]] = None,
        openapi_path: str = "/openapi.json",
        use_action_mask: bool = True,
        enforce_valid_actions: bool = True,
        invalid_action_penalty: float = -1.0,
        max_steps: Optional[int] = None,
        client: Optional[httpx.Client] = None,
        timeout: float = 30.0,
    ):
        """
        Args:
            backend_url: Base URL for the running backend (e.g., http://localhost:8000).
            api_slug: Generated API slug (used to scope actions to /generated/{slug}/*).
            goal: Goal payload used to create a goal if goal_id is not provided.
            goal_id: Existing goal ID to reuse.
            actions: Optional static action list; if omitted, actions are built from OpenAPI.
            openapi_path: Path to the backend OpenAPI doc (default /openapi.json).
            use_action_mask: Whether to query /valid-actions each step.
            enforce_valid_actions: If True, invalid actions are short-circuited with a penalty.
            invalid_action_penalty: Reward applied when an invalid action is attempted.
            max_steps: Optional cap; exceeding it sets truncated=True.
            client: Optional httpx.Client; otherwise a new one is created.
            timeout: Timeout (seconds) for HTTP calls when constructing the default client.
        """
        if not _GYM_AVAILABLE:
            raise ImportError(
                "gymnasium or gym is required for DeepMockGymEnv. "
                "Install with: pip install gymnasium"
            )
        super().__init__()
        self.backend_url = backend_url.rstrip("/")
        self.api_slug = api_slug
        self.goal_template = goal
        self.goal_id = goal_id
        self.use_action_mask = use_action_mask
        self.enforce_valid_actions = enforce_valid_actions
        self.invalid_action_penalty = float(invalid_action_penalty)
        self.max_steps = max_steps
        self._owned_client = client is None
        self.client = client or httpx.Client(base_url=self.backend_url, timeout=timeout)

        # Always discover actions from OpenAPI, then optionally merge with provided actions
        discovered_actions = self._load_actions_from_openapi(openapi_path)
        
        if actions:
            # Merge provided actions with discovered ones (provided actions take precedence for duplicates)
            # Create a lookup by action_id for discovered actions
            discovered_by_id = {
                (a.get("method", "").upper(), a.get("path", "")): a
                for a in discovered_actions
            }
            # Add/override with provided actions
            for action in actions:
                key = (action.get("method", "").upper(), action.get("path", ""))
                discovered_by_id[key] = action
            # Convert back to list
            merged_actions = list(discovered_by_id.values())
            self.actions = self._normalize_actions(merged_actions)
        else:
            self.actions = self._normalize_actions(discovered_actions)
        
        if not self.actions:
            raise ValueError("No actions discovered; provide an action list or ensure OpenAPI is reachable.")

        self.components = self._infer_components(self.actions)
        self.observation_space = self._build_observation_space(self.components)
        self.action_space = spaces.Discrete(len(self.actions))

        self._episode_id: Optional[str] = None
        self._steps = 0
        self._last_observation: Optional[Dict[str, Any]] = None
        self._last_response: Optional[Dict[str, Any]] = None

    # Gym API
    def reset(self, *, seed: Optional[int] = None, options: Optional[Dict[str, Any]] = None) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        super().reset(seed=seed)
        opts = options or {}

        if opts.get("goal"):
            self.goal_template = opts["goal"]
            self.goal_id = None
        if opts.get("goal_id"):
            self.goal_id = opts["goal_id"]

        goal_id = self.goal_id or self._create_goal()
        self.goal_id = goal_id
        self._episode_id = self._start_episode(goal_id)
        self._steps = 0

        raw_obs = self._fetch_observation()
        obs, obs_info = self._coerce_observation(raw_obs)
        self._last_observation = obs

        info = {"episode_id": self._episode_id, "goal_id": goal_id}
        if obs_info:
            info.update(obs_info)
        return obs, info

    def step(self, action: int) -> Tuple[Dict[str, Any], float, bool, bool, Dict[str, Any]]:
        if self._episode_id is None:
            raise RuntimeError("Call reset() before stepping the environment.")

        try:
            selected = self.actions[int(action)]
        except (IndexError, ValueError) as exc:
            raise ValueError(f"Action {action} is out of range for action space {self.action_space.n}.") from exc

        info: Dict[str, Any] = {"action_id": selected["action_id"]}

        valid_action_ids: Optional[List[str]] = None
        if self.use_action_mask:
            valid_action_ids = self._fetch_valid_action_ids()
            info["valid_action_ids"] = valid_action_ids
            if self.enforce_valid_actions and selected["action_id"] not in valid_action_ids:
                # Short-circuit invalid actions with a penalty and no state change
                self._steps += 1
                truncated = bool(self.max_steps is not None and self._steps >= self.max_steps)
                obs = self._last_observation or {}
                info["invalid_action"] = True
                return obs, self.invalid_action_penalty, False, truncated, info

        response = self._execute_action(selected)
        self._last_response = response

        reward = float(response.get("reward", 0.0))
        terminated = bool(response.get("done", False))
        reason = response.get("reason")
        http_status = response.get("response_status")
        if reason:
            info["reason"] = reason
        if http_status is not None:
            info["response_status"] = http_status

        raw_obs = self._fetch_observation()
        obs, obs_info = self._coerce_observation(raw_obs)
        self._last_observation = obs

        self._steps += 1
        truncated = bool(self.max_steps is not None and self._steps >= self.max_steps)

        if obs_info:
            info.update(obs_info)
        if valid_action_ids is not None:
            info.setdefault("valid_action_ids", valid_action_ids)
        return obs, reward, terminated, truncated, info

    def render(self) -> None:
        if self._last_response is None:
            return
        print(f"Last action response: {self._last_response}")

    def close(self) -> None:
        if self._owned_client:
            self.client.close()

    # Helpers
    def _create_goal(self) -> str:
        if not self.goal_template:
            raise ValueError("Goal configuration is required to create a goal.")

        payload = dict(self.goal_template)
        payload.setdefault("api_slug", self.api_slug)

        resp = self.client.post("/rl/goals", json=payload)
        resp.raise_for_status()
        data = resp.json()
        return data["goal_id"]

    def _start_episode(self, goal_id: str) -> str:
        resp = self.client.post(f"/rl/goals/{goal_id}/episodes", json={"goal_id": goal_id})
        resp.raise_for_status()
        return resp.json()["episode_id"]

    def _fetch_observation(self) -> Dict[str, Any]:
        resp = self.client.get(f"/rl/episodes/{self._episode_id}/observation")
        resp.raise_for_status()
        return resp.json()

    def _fetch_valid_action_ids(self) -> List[str]:
        payload = {"available_actions": self.actions}
        resp = self.client.post(f"/rl/episodes/{self._episode_id}/valid-actions", json=payload)
        resp.raise_for_status()
        data = resp.json()
        return list(data.get("valid_action_ids", []))

    def _execute_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        payload = {
            "method": action["method"],
            "path": action["path"],
            "params": action.get("params") or {},
            "body": action.get("body"),
            "headers": action.get("headers"),
        }
        resp = self.client.post(f"/rl/episodes/{self._episode_id}/actions", json=payload)
        if resp.status_code >= 400:
            return {
                "reward": self.invalid_action_penalty,
                "done": False,
                "reason": resp.text,
                "response_status": resp.status_code,
                "response_body": None,
            }
        return resp.json()

    def _normalize_actions(self, actions: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
        normalized: List[Dict[str, Any]] = []
        seen_ids: set[str] = set()
        for idx, action in enumerate(actions):
            method = action.get("method")
            path = action.get("path", "/")
            if not method:
                raise ValueError("Each action must include a HTTP method.")

            method = str(method).upper()
            normalized_path = _normalize_path(self.api_slug, path)
            action_id = action.get("action_id") or f"{method}:{normalized_path}"
            if action_id in seen_ids:
                action_id = f"{action_id}#{idx}"
            seen_ids.add(action_id)

            normalized.append(
                {
                    "action_id": action_id,
                    "method": method,
                    "path": normalized_path,
                    "params": action.get("params"),
                    "body": action.get("body"),
                    "headers": action.get("headers"),
                    "summary": action.get("summary"),
                }
            )
        return normalized

    def _infer_components(self, actions: Iterable[Dict[str, Any]]) -> List[str]:
        components: set[str] = set()
        for action in actions:
            component = _component_from_path(str(action.get("path", "")))
            if component:
                components.add(component)
        return sorted(components)

    def _build_observation_space(self, components: Sequence[str]) -> spaces.Dict:
        known_id_spaces = {component: spaces.Sequence(spaces.Text(max_length=128)) for component in components}
        return spaces.Dict(
            {
                "required": spaces.Sequence(spaces.Text(max_length=64)),
                "satisfied": spaces.Sequence(spaces.Text(max_length=64)),
                "known_ids": spaces.Dict(known_id_spaces),
                "last_k_components": spaces.Sequence(spaces.Text(max_length=64)),
                "last_action_id": spaces.Text(max_length=128),
                "last_status": spaces.Box(low=-1e9, high=1e9, shape=(), dtype=np.int32),
                "steps_remaining": spaces.Box(low=0, high=1e6, shape=(), dtype=np.int32),
            }
        )

    def _coerce_observation(self, obs: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Project backend observation into the declared observation space."""
        processed = {
            "required": obs.get("required") or [],
            "satisfied": obs.get("satisfied") or [],
            "last_k_components": obs.get("last_k_components") or [],
            "last_action_id": obs.get("last_action_id") or "",
            "steps_remaining": int(obs.get("steps_remaining") or 0),
        }
        last_status = obs.get("last_status")
        processed["last_status"] = int(last_status) if last_status is not None else -1

        known_ids = obs.get("known_ids") or {}
        extra_known_ids = {k: v for k, v in known_ids.items() if k not in self.components}
        processed_known = {k: v for k, v in known_ids.items() if k in self.components}
        processed["known_ids"] = processed_known

        info: Dict[str, Any] = {}
        if extra_known_ids:
            info["dropped_known_ids"] = extra_known_ids

        top_k_routes = obs.get("top_k_routes")
        if top_k_routes:
            info["top_k_routes"] = top_k_routes

        return processed, info

    def _load_actions_from_openapi(self, openapi_path: str) -> List[Dict[str, Any]]:
        """Load all mutating actions (POST/PUT/PATCH/DELETE) from OpenAPI spec.
        
        Includes all routes for the API slug, including those with path parameters.
        """
        resp = self.client.get(openapi_path)
        resp.raise_for_status()
        schema = resp.json()
        paths = schema.get("paths", {})

        actions: List[Dict[str, Any]] = []
        prefix = f"/generated/{self.api_slug}"
        # Only include mutating methods (exclude GET for RL - we want actions that modify state)
        mutating_methods = {"post", "put", "patch", "delete"}
        
        for path, methods in paths.items():
            if not path.startswith(prefix):
                continue
            if not isinstance(methods, dict):
                continue
            for method, meta in methods.items():
                if method.lower() not in mutating_methods:
                    continue
                if not isinstance(meta, dict):
                    continue
                actions.append(
                    {
                        "method": method.upper(),
                        "path": path,
                        "summary": meta.get("summary"),
                    }
                )

        return actions
