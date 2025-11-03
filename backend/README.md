FastAPI Backend
===============

Prerequisites
-------------
- Python 3.12+

Setup
-----
1. Create a virtual environment (recommended)
   
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies
   
   ```bash
   pip install -r requirements.txt
   ```

Environment
-----------
Configure a PostgreSQL database and expose it as `DATABASE_URL`. Example:

```bash
export DATABASE_URL="postgresql+psycopg://user:password@localhost:5432/deepmock"
```

Run
---
- Start the FastAPI server (auto-reload enabled):
  
  ```bash
  python backend/main.py
  ```

- Or run via Uvicorn directly:
  
  ```bash
  uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
  ```

Containerised Generation Workflow
---------------------------------
1. Start your backend server (required for component ingestion):
   
   ```bash
   export DATABASE_URL="postgresql+psycopg://user:password@localhost:5432/deepmock"
   python backend/main.py
   ```

2. Upload OpenAPI spec to ingest components:
   
   ```bash
   curl -X POST "http://localhost:8000/apis/upload" \
     -F "spec_file=@path/to/openapi.json" \
     -F "api_name=Your API"
   ```

3. Build the backend image (contains the generator runtime and CLI tools):
   
   ```bash
   docker build -t deepmock-backend:latest backend
   ```

4. Generate API with Docker (uses your existing database with components):
   
   ```bash
   # Export your database URL so Docker can use it
   export _DATABASE_URL="postgresql+psycopg://user:password@localhost:5432/deepmock"
   
   # Run generation job
   python3 backend/scripts/run_generation_job.py \
     --api-slug stripe \
     --manifest backend/reverse/generated/stripe/plan/plan.json \
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
# View human-readable plan
curl -X POST "http://localhost:8000/reverse/plan" \
  -H "Content-Type: application/json" \
  -d '{"api_slug": "stripe"}'
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
curl -X POST "http://localhost:8000/reverse/generate" \
  -H "Content-Type: application/json" \
  -d '{"api_slug": "stripe"}'
```

**Or via Docker CLI:**

```bash
export _DATABASE_URL="postgresql+psycopg://user:password@localhost:5432/deepmock"

python3 backend/scripts/run_generation_job.py \
  --api-slug stripe \
  --manifest backend/reverse/generated/stripe/plan/plan.json \
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
curl "http://localhost:8000/reverse/preview?api_slug=stripe"
```

### Step 5: Apply to Main Backend (Optional)

Mount generated routes in the running FastAPI app:

```bash
curl -X POST "http://localhost:8000/reverse/apply" \
  -H "Content-Type: application/json" \
  -d '{"api_slug": "stripe"}'
```

This automatically:
- Validates the plan
- Generates code (routes, tests, services)
- Generates data for ALL components using dependency graph
- Stores data in `generated_records` table
- Syncs package to `generated_output/{api_slug}/` with standalone API (`main.py`, `runtime.py`)
- Mounts routes at `/generated/{api_slug}/*`

**Routes become available at:**
- `http://localhost:8000/generated/stripe/v1/...`

### Step 6: Standalone API (Recommended)

For a completely isolated deployment, run the standalone version:

```bash
cd generated_output/stripe
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


