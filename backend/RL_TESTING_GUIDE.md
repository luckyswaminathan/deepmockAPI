# Testing Guide for New RL Features

This guide explains how to test the new RL features: observations, action masking, transition logging, and reward shaping.

## Prerequisites

1. **Start the backend server** with RL enabled:
   ```bash
   # Option 1: Docker Compose (recommended)
   docker compose -f docker-compose.rl.yml up --build
   
   # Option 2: Manual
   cd backend
   export RL_ENABLED=true
   export REDIS_URL=redis://localhost:6379
   uvicorn main:app --reload
   ```

2. **Ensure you have test data**:
   - `backend/scripts/simple_account_goal.json` - Test goal
   - `backend/scripts/simple_account_actions.json` - Test actions

## Quick Test

Run the automated test script:

```bash
cd backend
python scripts/test_rl_features.py
```

This will:
1. Create a goal
2. Start an episode
3. Test observation encoding
4. Test action masking
5. Execute actions and test reward shaping
6. Test transition logging

## Manual Testing

### 1. Test Observation Encoding

```bash
# First, create a goal and start an episode
GOAL_ID="your_goal_id"
EPISODE_ID="your_episode_id"

# Get observation
curl http://localhost:8000/rl/episodes/${EPISODE_ID}/observation
```

Expected response:
```json
{
  "required": ["account", "customer"],
  "satisfied": [],
  "known_ids": {},
  "last_k_components": [],
  "last_action_id": null,
  "last_status": null,
  "steps_remaining": 2
}
```

### 2. Test Action Masking

```bash
# Get valid actions
curl -X POST http://localhost:8000/rl/episodes/${EPISODE_ID}/valid-actions \
  -H "Content-Type: application/json" \
  -d '{
    "available_actions": [
      {"method": "POST", "path": "/v1/accounts"},
      {"method": "POST", "path": "/v1/customers"},
      {"method": "GET", "path": "/v1/customers/{id}"}
    ]
  }'
```

Expected: Returns `valid_action_ids` array with actions that are valid at current state.

### 3. Test Reward Shaping

Execute actions and observe rewards:

```bash
# Execute an action
curl -X POST http://localhost:8000/rl/episodes/${EPISODE_ID}/actions \
  -H "Content-Type: application/json" \
  -d '{
    "method": "POST",
    "path": "/v1/accounts",
    "body": {"type": "express", "country": "US"}
  }'
```

Check the reward in the response. After executing the same action twice, the second time should NOT reward component completion (farming prevention).

### 4. Test Transition Logging

```bash
# Get transitions for episode
curl http://localhost:8000/rl/episodes/${EPISODE_ID}/transitions
```

Expected response includes:
- `transitions`: Array of transition objects with `state_id`, `obs`, `action_id`, `reward`, `done`, `next_state_id`, `info`
- `total_steps`: Number of transitions
- `total_reward`: Sum of all rewards
- `final_done`: Whether episode is done

## What to Verify

### Observation Encoding ✓
- [ ] Observation includes `required` components from goal
- [ ] Observation includes `satisfied` components (updates after actions)
- [ ] Observation includes `known_ids` (IDs discovered so far)
- [ ] Observation includes `last_k_components` (recent history)
- [ ] `steps_remaining` decreases as components are satisfied

### Action Masking ✓
- [ ] POST to collection endpoints are valid before component exists
- [ ] GET/PUT/PATCH/DELETE with path params are only valid if IDs exist
- [ ] Templated routes require all needed IDs

### Reward Shaping ✓
- [ ] Component completion reward only given on first satisfaction (no farming)
- [ ] Step penalty (-0.01) applied each step
- [ ] Failure penalty (-0.2 for 4xx, -0.3 for 5xx) applied on errors
- [ ] Rewards accumulate correctly

### Transition Logging ✓
- [ ] Transitions logged after each action
- [ ] Each transition has: `state_id`, `obs`, `action_id`, `reward`, `done`, `next_state_id`, `info`
- [ ] Transitions saved to file when episode completes
- [ ] Can retrieve transitions via API

## Using the Test Script

The test script (`test_rl_features.py`) provides comprehensive testing:

```bash
# Test with default files
python scripts/test_rl_features.py

# Test with custom files
python scripts/test_rl_features.py \
  --goal-file path/to/goal.json \
  --actions-file path/to/actions.json

# Test existing episode
python scripts/test_rl_features.py --episode-id episode_abc123
```

## Troubleshooting

1. **"RL routes not found"**: Make sure `RL_ENABLED=true` is set
2. **"Redis connection failed"**: Ensure Redis is running on `localhost:6379`
3. **"Episode not found"**: Make sure you're using a valid episode ID
4. **"No transitions"**: Execute some actions first, then check transitions

## Next Steps

After testing, you can:
1. Export rollout datasets for training: Check `TransitionLogger.export_rollout_dataset()`
2. Use observations in your policy: Call `/rl/episodes/{id}/observation`
3. Use action masks: Call `/rl/episodes/{id}/valid-actions` before selecting actions
4. Train PPO: Use the transition logs saved to `/tmp/rl_rollouts/` (or custom log_dir)

