# DeepMock API

**DeepMock** is an intelligent API reverse-engineering and code generation platform that transforms OpenAPI specifications into fully functional mock APIs with Reinforcement Learning (RL) capabilities.

## What DeepMock Does

DeepMock automates the creation of mock API servers from OpenAPI specifications, enabling:

### 🎯 Core Features

1. **Automatic API Generation**
   - Upload any OpenAPI 3.0 specification (JSON/YAML)
   - Automatically generates FastAPI routes, services, and handlers
   - Creates realistic sample data using component dependency graphs
   - Produces standalone, runnable mock API servers

2. **Intelligent Code Generation**
   - Reverse-engineers database operations from API routes
   - Infers CRUD operations, relationships, and constraints
   - Generates type-safe Python code with proper error handling
   - Creates test suites for generated routes

3. **Reinforcement Learning Integration**
   - Tracks API state changes automatically via middleware
   - Stores state transitions in Redis for RL training
   - Enables goal-based RL agents to learn API interactions
   - Provides reward calculation and episode management

4. **Component-Based Architecture**
   - Parses OpenAPI schemas into component registries
   - Builds dependency graphs between components
   - Generates coherent test data respecting relationships
   - Visualizes component relationships and API structure

### 🚀 Use Cases

- **API Development**: Quickly prototype and test API designs before implementing real backends
- **Testing**: Generate mock APIs for integration testing and CI/CD pipelines
- **RL Training**: Train reinforcement learning agents to interact with APIs
- **Documentation**: Explore API structures and relationships interactively
- **Education**: Learn API design patterns and OpenAPI specifications

### 🏗️ Architecture

```
OpenAPI Spec → Component Registry → Code Generation → Mock API Server
                    ↓
              State Tracking (Redis) → RL Training
```

The system uses:
- **FastAPI** for the backend and generated APIs
- **SQLite/PostgreSQL** for component and data storage
- **Redis** for RL state tracking (with LFU eviction)
- **Next.js** for the web interface
- **Docker Compose** for easy deployment

---

## Quick Start

This repository contains a FastAPI backend (with background generation jobs) and a Next.js frontend. The whole stack runs by starting the Docker Compose services from the repo root and then launching the frontend dev server.

## Prerequisites
- Docker + Docker Compose
- Node.js 18+ and npm (frontend only)

## 1. Run Backend Stack via Docker Compose
From the repository root, bring up Redis and the FastAPI backend (which now uses SQLite by default):

```bash
docker compose -f docker-compose.rl.yml up --build
```

What this does:
- Builds the backend image if needed and starts it with live reload
- Mounts `backend/deepmock.db` into the container and uses it as the SQLite datastore
- Provisions Redis (`localhost:6379`) for RL flows
- Exposes the FastAPI app at `http://localhost:8000`

The logs for every service stream in the same terminal. When you are done, stop everything with `Ctrl+C` and optionally clean up with:

```bash
docker compose -f docker-compose.rl.yml down
```

## 2. Run the Frontend
With the backend stack running, start the Next.js app in a second terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:3000` and is already configured to talk to the backend at `http://localhost:8000`.

## Upload an OpenAPI Specification
1. Open `http://localhost:3000/upload` and select your OpenAPI JSON/YAML file, or
2. Use the API directly:

```bash
curl -X POST "http://localhost:8000/apis/upload" \
  -F "spec_file=@path/to/your/openapi.json" \
  -F "api_name=Your API Name"
```

After a successful upload the API appears on the home page (`/`) where you can explore components.

## Generate Mock API Assets
Build (once) and run the generation script, replacing `{api_slug}` with the slug returned by the upload response:

```bash
docker compose -f docker-compose.rl.yml build backend  # only if you need a fresh image

python3 backend/scripts/run_generation_job.py \
  --api-slug {api_slug} \
  --manifest backend/reverse/generated/{api_slug}/plan/plan.json \
  --output-dir ./generated_output
```

By default the script reads `_DATABASE_URL` / `DATABASE_URL`. If neither is set it falls back to the shared SQLite file at `backend/deepmock.db`, mounts it into the container, and rewrites the DSN automatically. Pass `--database-backend postgres` if you still want a transient Postgres container. The job generates code, data, and assets and syncs them into `generated_output/{api_slug}/`.

## Alternative: Trigger Generation via API
```bash
curl -X POST "http://localhost:8000/reverse/plan" \
  -H "Content-Type: application/json" \
  -d '{"api_slug": "{api_slug}"}'

curl -X POST "http://localhost:8000/reverse/generate" \
  -H "Content-Type: application/json" \
  -d '{"api_slug": "{api_slug}"}'
```

To run a standalone generated API:
```bash
cd generated_output/{api_slug}
pip install -r requirements.txt
python main.py
```

## RL (Reinforcement Learning) Features

DeepMock includes built-in RL capabilities for training agents to interact with APIs:

### Enable RL Mode

RL is automatically enabled when using `docker-compose.rl.yml`. For manual setup:

```bash
export RL_ENABLED=true
export REDIS_URL=redis://localhost:6379/0
```

### RL Workflow

1. **Automatic State Tracking**: All API calls to `/generated/{api_slug}/*` are automatically tracked
2. **Create Goals**: Define target states using the `/rl/goals` endpoint
3. **Run Episodes**: Train RL agents to reach goals via `/rl/episodes`
4. **Export Data**: Export RL training data for model fine-tuning

### Example: Create a Goal

```bash
curl -X POST "http://localhost:8000/rl/goals" \
  -H "Content-Type: application/json" \
  -d '{
    "api_slug": "stripe",
    "description": "Create a customer with payment method",
    "goal_state": {
      "target_components": {
        "customer": [{"id": "cus_*", "email": "customer@example.com"}],
        "payment_method": [{"id": "pm_*", "customer": "cus_*", "type": "card"}]
      }
    }
  }'
```

See `backend/RL_GOAL_EXAMPLES.md` for more examples.

### RL Endpoints

- `POST /rl/goals` - Create a new goal
- `POST /rl/episodes` - Start an RL episode
- `POST /rl/episodes/{episode_id}/actions` - Execute an action
- `GET /rl/states/{state_id}` - Get state information
- `POST /rl/states/{state_id}/restore` - Restore database to a state

## Useful Notes
- Backend CORS already allows `http://localhost:3000`.
- All generated data is stored inside `backend/deepmock.db` (SQLite) and mirrored to `generated_output/`.
- Use `_DATABASE_URL`/`DATABASE_URL` to point to a different SQLite or Postgres instance if desired.
- RL state tracking requires Redis (automatically provisioned in Docker Compose).
- Generated APIs are automatically mounted at `/generated/{api_slug}/*` when the server starts.
- Uploading an API automatically generates code, data, and initial RL state - no separate generation step needed!

## Project Structure
```
backend/
  main.py            # FastAPI app + routes
  database.py        # SQLAlchemy engine & tables
  ingestion.py       # OpenAPI ingestion → tables + registries
  reverse/           # Code generation pipeline
frontend/
  src/app/           # Next.js App Router pages
  src/lib/api.ts     # Frontend fetch helpers
generated_output/   # Generated standalone APIs
  {api_slug}/
    main.py          # Standalone FastAPI app
    runtime.py       # In-memory storage
    code/            # Generated routes
```
