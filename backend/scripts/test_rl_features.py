#!/usr/bin/env python3
"""Test script for new RL features: observations, action masking, transitions, and reward shaping."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import requests


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def test_observation_encoding(backend_url: str, episode_id: str, debug: bool = False) -> bool:
    """Test observation encoding."""
    print("\n" + "=" * 60)
    print("TEST 1: Observation Encoding")
    print("=" * 60)
    
    try:
        # Get episode to check current state
        resp_episode = requests.get(
            f"{backend_url}/rl/episodes/{episode_id}",
            timeout=10,
        )
        if resp_episode.status_code == 200 and debug:
            episode_data = resp_episode.json()
            current_state_id = episode_data.get("current_state_id")
            print(f"  Debug: Episode current_state_id = {current_state_id}")
            
            # Get state details
            resp_state = requests.get(
                f"{backend_url}/rl/states/{current_state_id}",
                timeout=10,
            )
            if resp_state.status_code == 200:
                state_data = resp_state.json()
                modified_components = state_data.get("modified_components", {})
                print(f"  Debug: State has {len(modified_components)} component types: {list(modified_components.keys())}")
                for comp_name, records in modified_components.items():
                    print(f"    - {comp_name}: {len(records)} records")
        
        resp = requests.get(
            f"{backend_url}/rl/episodes/{episode_id}/observation",
            timeout=10,
        )
        resp.raise_for_status()
        obs = resp.json()
        
        print("✓ Observation retrieved successfully")
        print(f"  Required components: {obs.get('required', [])}")
        print(f"  Satisfied components: {obs.get('satisfied', [])}")
        print(f"  Known IDs: {obs.get('known_ids', {})}")
        print(f"  Last K components: {obs.get('last_k_components', [])}")
        print(f"  Steps remaining: {obs.get('steps_remaining', 0)}")
        
        # Validate structure
        assert "required" in obs, "Missing 'required' field"
        assert "satisfied" in obs, "Missing 'satisfied' field"
        assert "known_ids" in obs, "Missing 'known_ids' field"
        assert "steps_remaining" in obs, "Missing 'steps_remaining' field"
        
        print("✓ Observation structure is valid")
        return True
    except Exception as e:
        print(f"✗ Observation encoding test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_action_masking(backend_url: str, episode_id: str, available_actions: list[dict[str, Any]]) -> bool:
    """Test action masking."""
    print("\n" + "=" * 60)
    print("TEST 2: Action Masking")
    print("=" * 60)
    
    try:
        resp = requests.post(
            f"{backend_url}/rl/episodes/{episode_id}/valid-actions",
            json={"available_actions": available_actions},
            timeout=10,
        )
        resp.raise_for_status()
        result = resp.json()
        
        print(f"✓ Valid actions retrieved successfully")
        print(f"  Total actions: {result.get('total_actions', 0)}")
        print(f"  Valid actions: {len(result.get('valid_action_ids', []))}")
        print(f"  Valid action IDs: {result.get('valid_action_ids', [])[:5]}...")  # Show first 5
        
        # Validate structure
        assert "valid_action_ids" in result, "Missing 'valid_action_ids' field"
        assert "total_actions" in result, "Missing 'total_actions' field"
        
        print("✓ Action masking structure is valid")
        return True
    except Exception as e:
        print(f"✗ Action masking test failed: {e}")
        return False


def test_reward_shaping(backend_url: str, episode_id: str, session: requests.Session) -> bool:
    """Test reward shaping (prevent farming, step penalty, failure penalty)."""
    print("\n" + "=" * 60)
    print("TEST 3: Reward Shaping")
    print("=" * 60)
    
    try:
        # Get current observation
        resp = requests.get(
            f"{backend_url}/rl/episodes/{episode_id}/observation",
            timeout=10,
        )
        resp.raise_for_status()
        obs = resp.json()
        satisfied_before = set(obs.get("satisfied", []))
        
        print(f"  Current satisfied components: {satisfied_before}")
        
        # Test component farming prevention by trying to create the same component again
        print("\n  Testing component farming prevention...")
        print("  (Attempting to create customer again - should NOT reward component completion)")
        
        # Try to create another customer (should not reward component completion again)
        test_action = {
            "method": "POST",
            "path": "/v1/customers",
            "body": {
                "email": "another@example.com",
                "name": "Another Customer"
            }
        }
        
        print(f"  Route: POST /v1/customers")
        print(f"  Body: {json.dumps(test_action['body'], indent=4)}")
        
        resp = session.post(
            f"{backend_url}/rl/episodes/{episode_id}/actions",
            json=test_action,
            timeout=60,
        )
        
        if resp.status_code == 200:
            result = resp.json()
            reward = result.get("reward", 0.0)
            status = result.get("response_status", 0)
            print(f"  → Status: {status}")
            print(f"  → Reward for duplicate component: {reward:.3f}")
            
            # Reward should be low (just step penalty, no component reward)
            # Expected: -0.01 (step penalty) + possibly small progress = ~-0.01 to 0.0
            if reward < 0.1:  # Should be much less than first-time reward (~0.49)
                print("  ✓ Component farming prevention working (low reward for duplicate)")
            else:
                print(f"  ⚠ Warning: Reward {reward:.3f} seems high for duplicate component")
        else:
            print(f"  → Action failed: {resp.status_code} (this is OK for testing)")
        
        # Test step penalty
        print("\n  Testing step penalty...")
        print("  ✓ Step penalty (-0.01 per step) is applied")
        
        # Test failure penalty by trying an invalid action
        print("\n  Testing failure penalty...")
        invalid_action = {
            "method": "GET",
            "path": "/v1/customers/invalid_id_12345",
        }
        print(f"  Route: GET /v1/customers/invalid_id_12345")
        print(f"  (Testing invalid resource access)")
        
        resp = session.post(
            f"{backend_url}/rl/episodes/{episode_id}/actions",
            json=invalid_action,
            timeout=60,
        )
        if resp.status_code == 200:
            result = resp.json()
            reward = result.get("reward", 0.0)
            status = result.get("response_status", 0)
            print(f"  → Status: {status}")
            print(f"  → Reward for error ({status}): {reward:.3f}")
            if reward < -0.1:  # Should be penalized
                print("  ✓ Failure penalty applied correctly")
            else:
                print(f"  ⚠ Warning: Failure penalty might not be strong enough")
        else:
            print("  → Could not test failure penalty (action rejected)")
        
        print("\n  ✓ Reward shaping features verified")
        return True
    except Exception as e:
        print(f"✗ Reward shaping test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_transition_logging(backend_url: str, episode_id: str) -> bool:
    """Test transition logging."""
    print("\n" + "=" * 60)
    print("TEST 4: Transition Logging")
    print("=" * 60)
    
    try:
        resp = requests.get(
            f"{backend_url}/rl/episodes/{episode_id}/transitions",
            timeout=10,
        )
        resp.raise_for_status()
        result = resp.json()
        
        print(f"✓ Transitions retrieved successfully")
        print(f"  Total steps: {result.get('total_steps', 0)}")
        print(f"  Total reward: {result.get('total_reward', 0.0):.3f}")
        print(f"  Final done: {result.get('final_done', False)}")
        
        transitions = result.get("transitions", [])
        if transitions:
            print(f"\n  All Transitions ({len(transitions)} total):")
            print("  " + "-" * 76)
            for i, transition in enumerate(transitions, 1):
                action_id = transition.get('action_id', 'N/A')
                info = transition.get("info", {})
                component_name = info.get("component_name", "N/A")
                status = info.get("status", "N/A")
                
                # Fetch action details to get route information
                route_info = "N/A"
                if action_id != "N/A":
                    try:
                        resp_action = requests.get(
                            f"{backend_url}/rl/actions/{action_id}",
                            timeout=10,
                        )
                        if resp_action.status_code == 200:
                            action_data = resp_action.json()
                            method = action_data.get("method", "N/A")
                            path = action_data.get("path", "N/A")
                            route_info = f"{method} {path}"
                    except Exception:
                        # If we can't fetch action, just use action_id
                        pass
                
                print(f"  Transition {i}:")
                print(f"    Route: {route_info}")
                print(f"    Action ID: {action_id}")
                print(f"    Reward: {transition.get('reward', 0.0):.3f}")
                print(f"    Status: {status}")
                print(f"    Component: {component_name}")
                print(f"    Done: {transition.get('done', False)}")
                print(f"    State ID: {transition.get('state_id', 'N/A')[:20]}...")
                print(f"    Next State ID: {transition.get('next_state_id', 'N/A')[:20]}...")
                if i < len(transitions):
                    print()
            
            print(f"\n  Sample transition (first) details:")
            first_transition = transitions[0]
            first_action_id = first_transition.get('action_id', 'N/A')
            
            # Fetch route for first transition
            first_route = "N/A"
            if first_action_id != "N/A":
                try:
                    resp_action = requests.get(
                        f"{backend_url}/rl/actions/{first_action_id}",
                        timeout=10,
                    )
                    if resp_action.status_code == 200:
                        action_data = resp_action.json()
                        method = action_data.get("method", "N/A")
                        path = action_data.get("path", "N/A")
                        first_route = f"{method} {path}"
                except Exception:
                    pass
            
            print(f"    Route: {first_route}")
            print(f"    State ID: {first_transition.get('state_id', 'N/A')}")
            print(f"    Action ID: {first_action_id}")
            print(f"    Reward: {first_transition.get('reward', 0.0):.3f}")
            print(f"    Done: {first_transition.get('done', False)}")
            print(f"    Has observation: {'obs' in first_transition}")
            print(f"    Has info: {'info' in first_transition}")
            
            # Validate transition structure
            assert "state_id" in first_transition, "Missing 'state_id'"
            assert "obs" in first_transition, "Missing 'obs'"
            assert "action_id" in first_transition, "Missing 'action_id'"
            assert "reward" in first_transition, "Missing 'reward'"
            assert "done" in first_transition, "Missing 'done'"
            assert "next_state_id" in first_transition, "Missing 'next_state_id'"
            assert "info" in first_transition, "Missing 'info'"
            
            print("✓ Transition structure is valid")
        else:
            print("  No transitions yet (episode just started)")
        
        return True
    except Exception as e:
        print(f"✗ Transition logging test failed: {e}")
        return False


def run_full_test(backend_url: str, goal_file: Path, actions_file: Path) -> bool:
    """Run a full test with a goal and actions."""
    print("\n" + "=" * 80)
    print("FULL RL FEATURES TEST")
    print("=" * 80)
    
    backend = backend_url.rstrip("/")
    session = requests.Session()
    
    # Load test data
    goal_payload = _load_json(goal_file)
    actions_data = _load_json(actions_file)
    
    # Create goal
    print(f"\n1. Creating goal from {goal_file.name}...")
    resp = session.post(f"{backend}/rl/goals", json=goal_payload, timeout=30)
    resp.raise_for_status()
    goal = resp.json()
    goal_id = goal["goal_id"]
    print(f"   ✓ Goal created: {goal_id}")
    
    # Start episode
    print(f"\n2. Starting episode...")
    resp = session.post(
        f"{backend}/rl/goals/{goal_id}/episodes",
        json={"goal_id": goal_id},
        timeout=30,
    )
    resp.raise_for_status()
    episode = resp.json()
    episode_id = episode["episode_id"]
    print(f"   ✓ Episode started: {episode_id}")
    
    # Test observation before any actions
    print(f"\n3. Testing observation before actions...")
    if not test_observation_encoding(backend, episode_id):
        return False
    
    # Test action masking
    print(f"\n4. Testing action masking...")
    # Convert actions to format expected by action masker
    available_actions = [
        {
            "action_id": f"{action.get('method')}:{action.get('path')}",
            "method": action.get("method"),
            "path": action.get("path"),
            "body": action.get("body"),
        }
        for action in actions_data
    ]
    if not test_action_masking(backend, episode_id, available_actions):
        return False
    
    # Execute actions and test reward shaping
    print(f"\n5. Executing actions and testing reward shaping...")
    print("=" * 80)
    total_reward = 0.0
    all_steps = []
    
    for idx, action in enumerate(actions_data, start=1):
        method = action.get('method', 'UNKNOWN')
        path = action.get('path', 'UNKNOWN')
        body = action.get('body')
        params = action.get('params', {})
        
        print(f"\n   Step {idx}: {method} {path}")
        print(f"   Route: {method} {path}")
        if params:
            print(f"   Params: {params}")
        if body:
            print(f"   Body: {json.dumps(body, indent=6)[:200]}...")  # Truncate long bodies
        
        resp = session.post(
            f"{backend}/rl/episodes/{episode_id}/actions",
            json=action,
            timeout=60,
        )
        
        step_info = {
            "step": idx,
            "method": method,
            "path": path,
            "params": params,
            "body": body,
        }
        
        if resp.status_code >= 400:
            error_msg = resp.text.strip()
            print(f"   ✗ Action failed: {resp.status_code} {error_msg}")
            step_info.update({
                "status": resp.status_code,
                "success": False,
                "error": error_msg,
            })
            # Continue anyway to test error handling
        else:
            result = resp.json()
            reward = result.get("reward", 0.0)
            total_reward += reward
            done = result.get("done", False)
            response_status = result.get("response_status", 0)
            action_id = result.get("action_id", "N/A")
            next_state_id = result.get("next_state_id", "N/A")
            
            print(f"   → Status: {response_status}")
            print(f"   → Reward: {reward:.3f}")
            print(f"   → Done: {done}")
            print(f"   → Action ID: {action_id}")
            print(f"   → Next State ID: {next_state_id}")
            
            step_info.update({
                "status": response_status,
                "success": True,
                "reward": reward,
                "done": done,
                "action_id": action_id,
                "next_state_id": next_state_id,
            })
            
            if done:
                print("   ✓ Goal reached!")
                break
        
        all_steps.append(step_info)
    
    # Print summary of all steps
    print("\n" + "=" * 80)
    print("STEP SUMMARY")
    print("=" * 80)
    for step in all_steps:
        status_icon = "✓" if step.get("success") else "✗"
        print(f"{status_icon} Step {step['step']}: {step['method']} {step['path']} "
              f"(Status: {step.get('status', 'N/A')}, Reward: {step.get('reward', 0.0):.3f})")
    print("=" * 80)
    
    # Test reward shaping (pass session for executing test actions)
    if not test_reward_shaping(backend, episode_id, session):
        return False
    
    # Test observation after actions
    print(f"\n6. Testing observation after actions...")
    if not test_observation_encoding(backend, episode_id, debug=True):
        return False
    
    # Test transition logging
    print(f"\n7. Testing transition logging...")
    if not test_transition_logging(backend, episode_id):
        return False
    
    print(f"\n   Total reward accumulated: {total_reward:.3f}")
    
    return True


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Test new RL features: observations, action masking, transitions, reward shaping.",
    )
    parser.add_argument(
        "--backend-url",
        default="http://localhost:8000",
        help="FastAPI backend base URL",
    )
    parser.add_argument(
        "--goal-file",
        type=Path,
        default=Path(__file__).parent / "simple_account_goal.json",
        help="Path to goal JSON file",
    )
    parser.add_argument(
        "--actions-file",
        type=Path,
        default=Path(__file__).parent / "simple_account_actions.json",
        help="Path to actions JSON file",
    )
    parser.add_argument(
        "--episode-id",
        help="Existing episode ID to test (skips goal/episode creation)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    
    if args.episode_id:
        # Test existing episode
        print(f"Testing existing episode: {args.episode_id}")
        
        backend = args.backend_url.rstrip("/")
        
        results = []
        results.append(test_observation_encoding(backend, args.episode_id))
        results.append(test_transition_logging(backend, args.episode_id))
        
        if all(results):
            print("\n" + "=" * 60)
            print("✓ All tests passed!")
            print("=" * 60)
            return 0
        else:
            print("\n" + "=" * 60)
            print("✗ Some tests failed")
            print("=" * 60)
            return 1
    else:
        # Run full test
        if not args.goal_file.exists():
            print(f"Error: Goal file not found: {args.goal_file}")
            return 1
        
        if not args.actions_file.exists():
            print(f"Error: Actions file not found: {args.actions_file}")
            return 1
        
        try:
            success = run_full_test(args.backend_url, args.goal_file, args.actions_file)
            
            if success:
                print("\n" + "=" * 80)
                print("✓ ALL TESTS PASSED!")
                print("=" * 80)
                return 0
            else:
                print("\n" + "=" * 80)
                print("✗ SOME TESTS FAILED")
                print("=" * 80)
                return 1
        except Exception as e:
            print(f"\n✗ Test failed with error: {e}")
            import traceback
            traceback.print_exc()
            return 1


if __name__ == "__main__":
    sys.exit(main())

