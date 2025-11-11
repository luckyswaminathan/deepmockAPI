# Current RL Functionality & What's Missing

## Current Functionality

### ✅ What Works

1. **Auto-Generation on Upload**
   - When you upload an API spec via `/apis/upload`, it automatically:
     - Ingests the spec
     - Generates code (routes, services)
     - Generates sample data
     - Syncs to `generated_apis/` and `generated_output/`
   - Routes are auto-mounted on server startup

2. **RL Middleware (Partially Working)**
   - Intercepts requests to `/generated/{api_slug}/*`
   - **NOW**: Automatically creates sessions for tracking
   - **NOW**: Automatically creates initial state if needed
   - Records actions (API calls) as state transitions
   - Stores states in Redis with LFU caching

3. **State Tracking**
   - States stored in Redis as `state:{state_id}`
   - Each state contains `modified_components` dict
   - States form a tree (parent → children)
   - Action path tracked (sequence of actions to reach state)

4. **RL API Endpoints**
   - `/rl/goals` - Create/manage goals
   - `/rl/episodes` - Manage RL episodes
   - `/rl/states` - Query states
   - `/rl/sessions` - Manage sessions

## What's Missing / Issues

### 🔴 Critical Missing Pieces

1. **Response Body Capture**
   - **Current**: Middleware doesn't capture response bodies
   - **Impact**: Can't track what data was created/updated
   - **Fix Needed**: Capture response body from FastAPI responses

2. **Initial State on API Generation**
   - **Current**: Initial state created on first API call
   - **Better**: Create initial state when API is generated/uploaded
   - **Impact**: First call might not track properly

3. **Component Detection**
   - **Current**: Tries to infer component from path
   - **Issue**: May not always be accurate
   - **Better**: Use route metadata from generated routes

4. **State Comparison Logic**
   - **Current**: Compares full database state
   - **Issue**: Slow for large datasets
   - **Better**: Track only what changed (delta)

### 🟡 Nice-to-Have Missing Features

5. **Response Body Streaming**
   - Can't capture streaming responses
   - Only works for JSON responses

6. **Error Handling**
   - If action tracking fails, request still succeeds (good)
   - But errors are silently logged - could be better

7. **State Deduplication**
   - Same state might be created multiple times
   - Should reuse existing states more efficiently

8. **Per-API State Isolation**
   - Currently uses per-API sessions, but states are global
   - Could be better organized per API

## Current Flow

```
1. Upload API → Auto-generates code + data
2. Server starts → Auto-mounts all generated APIs
3. API call → Middleware intercepts
   a. Creates/get session for API
   b. Gets current state (or creates initial)
   c. Executes request
   d. Records action
   e. Creates next state
   f. Updates session
4. State stored in Redis → Can query via /rl/states
```

## What Needs to Be Fixed

### ✅ Priority 1: Response Body Capture - COMPLETED
**Status**: Implemented
- Middleware now captures response body by wrapping the response stream
- Response body is captured as it streams and parsed as JSON
- Falls back to database state detection if response body unavailable
- **Note**: Response body may not be available immediately (streams async), but action tracker can use DB detection as fallback

### ✅ Priority 2: Initial State Creation - COMPLETED
**Status**: Implemented
- When API is uploaded/generated, initial state is created immediately
- Initial state includes seed data (if any) from data generation
- State is created in `/apis/upload` endpoint after data generation
- First API call will now use the pre-created initial state

### ✅ Priority 3: Better Component Detection - COMPLETED
**Status**: Implemented
- Middleware now extracts component name from route's docstring
- Looks for pattern: "Target component: {name}" in route docstring
- Falls back to path inference if docstring extraction fails
- More accurate component detection for state tracking

