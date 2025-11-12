FastAPI Backend
===============

Prerequisites
-------------
- Python 3.12+
- Docker (for database and generation)

Setup & Run
-----------

### Zero-Config RL Dev Stack (recommended)

Spin up PostgreSQL, Redis (pre-configured for LFU), and the backend—with `RL_ENABLED=true`—in one command using the root-level `docker-compose.rl.yml`:

```bash
# From repository root
docker compose -f docker-compose.rl.yml up --build
```

What you get:
- `postgres:16` with `deepmock/deepmock` credentials and a persistent `deepmock_pg` volume
- `redis:7` configured with the LFU eviction policy the RL tracker expects
- `uvicorn backend.main:app` running on `http://localhost:8000` with `RL_ENABLED=true`, `_DATABASE_URL`, and `REDIS_URL` already wired to the containers

Once the stack is healthy you can immediately upload an OpenAPI file, auto-generate mock routes, and use the `/rl/*` endpoints without any extra environment setup. Stop everything with `Ctrl+C`, or run in the background via `docker compose -f docker-compose.rl.yml up -d`.

### Manual setup

### 1. Initialize Database with Docker

Start a local PostgreSQL instance:

```bash
docker run --name deepmock-postgres \
  -e POSTGRES_USER=deepmock \
  -e POSTGRES_PASSWORD=deepmock \
  -e POSTGRES_DB=deepmock \
  -p 5432:5432 \
  -v deepmock_pg:/var/lib/postgresql/data \
  -d postgres:16
```

Set the database URL:

```bash
export DATABASE_URL="postgresql+psycopg://deepmock:deepmock@localhost:5432/deepmock"
```

### 2. Start Backend Server

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

The server will start at `http://localhost:8000`

### 3. Upload OpenAPI Specification

**Option A: Via API (curl)**

```bash
curl -X POST "http://localhost:8000/apis/upload" \
  -F "spec_file=@path/to/your/openapi.json" \
  -F "api_name=Your API Name"
```

**Option B: Via Frontend**

```bash
cd frontend
npm install
npm run dev
```

Then visit `http://localhost:3000/upload` to upload via the web UI.

### 4. Generate Mock API

Build the Docker image:

```bash
docker build -t deepmock-backend:latest backend
```

Run generation (replace `{api_slug}` with your actual API slug from the upload response):

```bash
export _DATABASE_URL="postgresql+psycopg://deepmock:deepmock@localhost:5432/deepmock"

python3 backend/scripts/run_generation_job.py \
  --api-slug {api_slug} \
  --manifest backend/reverse/generated/{api_slug}/plan/plan.json \
  --output-dir ./generated_output
```

**Note:** The script automatically detects `_DATABASE_URL` or `DATABASE_URL` from your environment
and uses your existing database (with `localhost` converted to `host.docker.internal` for Docker).
If no database URL is set, it creates a transient empty PostgreSQL container.

**What happens:**
- Generates code (routes, tests, services)
- Automatically generates data for ALL components using dependency graph
- Stores data in `generated_records` table
- Syncs to `generated_output/{api_slug}/` with standalone API files

OpenAPI Ingestion Workflow
---------------------------
1. Visit `http://localhost:8000/` for the dashboard.
2. Upload an OpenAPI JSON or YAML file. Optionally provide a display name.
3. The backend parses `components.schemas` and stores each component in PostgreSQL as a JSONB record,
   attaching a vendor field `x-deepmock-properties` that captures the derived property summary. No
   per-component tables are created, so large specs remain lightweight.
4. Browse the ingested APIs and their component summaries directly from the dashboard. You can also
   query the REST endpoints:
   - `POST /apis/upload` – ingest a specification.
   - `GET /apis` – list registered APIs.
   - `GET /apis/{api_slug}/components` – list stored components for an API (property counts included).
   - `GET /apis/{api_slug}/components/{component_name}` – view the JSON schema snapshot and property table.

Reverse Engineering & Code Generation Pipeline
-----------------------------------------------
The reverse engineering system can generate a complete mock API implementation from an uploaded OpenAPI spec.

### Step 1: Upload (Automatic Plan Generation)

When you upload an OpenAPI spec via `POST /apis/upload`, the system:
- Ingests components into the registry
- Generates a route inventory from the OpenAPI paths
- Automatically creates an initial generation plan using LLM inference

The plan is stored at `backend/reverse/generated/{api_slug}/plan/plan.json`

### Step 2: Review Plan (Optional)

Review the generated plan before code generation:

```bash
# View human-readable plan (replace {api_slug} with your API slug)
curl -X POST "http://localhost:8000/reverse/plan" \
  -H "Content-Type: application/json" \
  -d '{"api_slug": "{api_slug}"}'
```

The plan describes:
- Inferred database operations (CRUD) per route
- Component relationships and dependencies
- Data flow and transformations

Files:
- `plan/plan.json` - Machine-readable plan
- `plan/plan.md` - Human-readable documentation

### Step 3: Generate Code, Tests, and Data

**Via API (recommended):**

```bash
# Replace {api_slug} with your API slug
curl -X POST "http://localhost:8000/reverse/generate" \
  -H "Content-Type: application/json" \
  -d '{"api_slug": "{api_slug}"}'
```

**Or via Docker CLI:**

```bash
export _DATABASE_URL="postgresql+psycopg://deepmock:deepmock@localhost:5432/deepmock"

# Replace {api_slug} with your API slug
python3 backend/scripts/run_generation_job.py \
  --api-slug {api_slug} \
  --manifest backend/reverse/generated/{api_slug}/plan/plan.json \
  --output-dir ./generated_output
```

**Note:** Both methods automatically generate data for ALL components and store in `generated_records` table.

**Output Structure:**
```
backend/reverse/generated/{api_slug}/
├── code/
│   ├── routes.py      # FastAPI route handlers
│   └── services.py    # Business logic
├── tests/
│   └── test_routes.py # Pytest test stubs
├── data/
│   ├── generators/    # Deterministic data generators
│   └── seeds/         # Sample JSON fixtures
├── prompts/           # LLM prompt transcripts
├── plan/              # Generation plan (from step 1-2)
└── README.md          # Generated documentation
```

### Step 4: Preview (Optional)

Preview generated assets before applying:

```bash
# Replace {api_slug} with your API slug
curl "http://localhost:8000/reverse/preview?api_slug={api_slug}"
```

### Step 5: Apply to Main Backend (Optional)

Mount generated routes in the running FastAPI app:

```bash
# Replace {api_slug} with your API slug
curl -X POST "http://localhost:8000/reverse/apply" \
  -H "Content-Type: application/json" \
  -d '{"api_slug": "{api_slug}"}'
```

This automatically:
- Validates the plan
- Generates code (routes, tests, services)
- Generates data for ALL components using dependency graph
- Stores data in `generated_records` table
- Syncs package to `generated_output/{api_slug}/` with standalone API (`main.py`, `runtime.py`)
- Mounts routes at `/generated/{api_slug}/*`

**Routes become available at:**
- `http://localhost:8000/generated/{api_slug}/v1/...`

### Step 6: Standalone API (Recommended)

For a completely isolated deployment, run the standalone version:

```bash
# Replace {api_slug} with your API slug
cd generated_output/{api_slug}
pip install -r requirements.txt
python main.py
```

**Benefits:**
- No database required (in-memory storage)
- Self-contained FastAPI application
- Easy to deploy independently
- Perfect for development and testing

See `generated_output/{api_slug}/README_STANDALONE.md` for details.

### Additional Endpoints

- `POST /reverse/generate_data` - Generate sample data only (with custom counts/seed)
- `POST /reverse/cleanup` - Remove all generated assets for an API
- `GET /reverse/preview?api_slug={slug}` - Preview generated code structure

### Generation Process Details

**Planner (`reverse/planner.py`):**
- Uses LLM to infer CRUD operations from OpenAPI routes
- Maps request/response schemas to component registry
- Builds operation plan with validation

**Generator (`reverse/generator.py`):**
- Renders FastAPI route handlers from plan
- Generates route stubs with proper HTTP methods and path parameters
- Creates service layer scaffolding

**Data Synthesizer (`reverse/data_synthesizer.py`):**
- Generates deterministic sample data
- Follows component dependency graph (leaves first)
- Creates coherent fixture datasets

**Package Manager (`reverse/package_manager.py`):**
- Syncs generated code to `generated_output/`
- Creates standalone API structure with `main.py` and `runtime.py`

Visit
-----
- Dashboard & health: `http://localhost:8000/`
- Interactive docs (Swagger): `http://localhost:8000/docs`
- Alternative docs (ReDoc): `http://localhost:8000/redoc`

RL Dataset Export & Fine-Tuning
-------------------------------
Once RL tracking is enabled (`RL_ENABLED=true`) and you have collected one or more episodes through `/rl/episodes/{episode_id}/actions`, convert those rollouts into JSONL corpora and trigger OpenAI jobs with the helper scripts under `backend/scripts/`.

### 1. Export JSONL datasets

```bash
# Discover every stored episode (or pass --episode-id for a subset)
python3 backend/scripts/export_rl_dataset.py \
  --discover-all \
  --output-dir generated_output/datasets \
  --sft-min-reward 0.8
```

Outputs:
- `generated_output/datasets/sft.jsonl`: chat-formatted demonstrations (system prompt + goal/state context → HTTP call) filtered by reward or terminal success.
- `generated_output/datasets/ppo.jsonl`: transition-level rows with prompt, completion, shaped reward, done flag, and metadata (`episode_id`, `state_id`, `next_state_id`, etc.).

Useful flags:
- `--episode-id` (repeatable) / `--episodes-file` limit the export set.
- `--goal-id` filters by goal.
- `--done-only` keeps only terminal transitions in the SFT output. `--skip-sft` / `--skip-ppo` disable either file entirely.

### 2. Upload + kick off fine-tunes

```bash
OPENAI_API_KEY=sk-... python3 backend/scripts/push_finetune.py \
  --sft-file generated_output/datasets/sft.jsonl \
  --sft-model gpt-4.1-mini \
  --sft-suffix deepmock-stripe \
  --ppo-file generated_output/datasets/ppo.jsonl \
  --ppo-model ft:gpt-4.1-mini:your-org:deepmock-stripe \
  --ppo-algorithm ppo
```

Behavior:
- Each dataset is uploaded via `POST /v1/files` with the supplied purpose (`fine-tune` or `rl`).
- Supplying an SFT file immediately triggers `POST /v1/fine_tuning/jobs` and prints the resulting model id (or pending placeholder) so you can reuse it for PPO.
- Supplying a PPO file starts `POST /v1/rl/fine_tuning/jobs` against the provided (or freshly created) model using the algorithm you pass (`ppo` by default).
- `--dry-run` prints the plan without hitting the API—handy for CI rehearsals.

This closes the “collect → export → fine-tune” loop without leaving the repo.
