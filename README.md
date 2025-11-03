# DeepMock API – Local Development

This repository contains a FastAPI backend and a Next.js frontend. Follow the steps below to run everything locally.

## Prerequisites

- Docker
- Python 3.12+
- Node.js 18+ and npm
- Optional: `psql` CLI (for database health checks)

## 1) Start Postgres

Run a local Postgres instance on host port 5433 with a persistent volume:

```bash
docker run --name deepmock-postgres \
  -e POSTGRES_USER=xxxxx \
  -e POSTGRES_PASSWORD=xxxxx \
  -e POSTGRES_DB=deepmock \
  -p 5433:5432 \
  -v deepmock_pg:/var/lib/postgresql/data \
  -d postgres:16
```

Health check (optional):

```bash
PGPASSWORD=xxxxx psql 'postgresql://xxxxx@localhost:5433/xxxxx' -c 'select 1;'
```

## 2) Configure backend

Export the SQLAlchemy connection string (psycopg v3):

```bash
export DATABASE_URL='postgresql+psycopg://xxxxx:xxxxx@localhost:5433/xxxxx'
```

Install dependencies and run the API:

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Notes
- Core tables are created automatically on startup.
- CORS is enabled for `http://localhost:3000`.

## 3) Configure frontend

In a separate terminal:

```bash
cd frontend
npm install
# Optional if different from default
# export NEXT_PUBLIC_BACKEND_URL='http://localhost:8000'
npm run dev
```

Open `http://localhost:3000` in your browser.

## 4) Use the app

### Basic Workflow (Component Inspection)

- Upload an OpenAPI spec at `/upload` (JSON or YAML). Optionally provide a friendly API name.
- After a successful upload, see the API listed on the home page `/`.
- Click into an API to view its components and open a component to inspect its properties.

### Full Pipeline: Upload → Generation → Standalone API

The complete workflow to generate a runnable mock API from an OpenAPI specification:

#### Step 1: Upload and Ingest OpenAPI Spec

Upload your OpenAPI specification via the web UI (`/upload`) or API:

```bash
# Via API endpoint
curl -X POST "http://localhost:8000/apis/upload" \
  -F "spec_file=@path/to/your/openapi.json" \
  -F "api_name=Stripe API"
```

This automatically:
- Ingests the spec into the component registry
- Generates a route inventory
- Creates an initial generation plan

**Response includes:**
- `api_slug`: Unique identifier for the API (e.g., `stripe`)
- `api_name`: Display name
- `components`: List of discovered components with property counts

#### Step 2: Review the Generation Plan (Optional)

View the human-readable plan that describes inferred database operations:

```bash
# Via API endpoint
curl -X POST "http://localhost:8000/reverse/plan" \
  -H "Content-Type: application/json" \
  -d '{"api_slug": "stripe"}'
```

The plan is also available at:
- **Markdown**: `backend/reverse/generated/{api_slug}/plan/plan.md`
- **JSON**: `backend/reverse/generated/{api_slug}/plan/plan.json`

#### Step 3: Generate Code, Tests, and Sample Data

Generate the complete implementation:

```bash
# Via API endpoint
curl -X POST "http://localhost:8000/reverse/generate" \
  -H "Content-Type: application/json" \
  -d '{"api_slug": "stripe"}'
```

This generates:
- **`code/`**: FastAPI route handlers, services, and models
- **`tests/`**: Pytest test stubs
- **`data/`**: Data generators and seed files
- **`prompts/`**: LLM prompt transcripts for reproducibility

All output is written to `backend/reverse/generated/{api_slug}/`

#### Step 4: Preview Generated Assets (Optional)

Preview the generated code before applying:

```bash
curl "http://localhost:8000/reverse/preview?api_slug=stripe"
```

#### Step 5: Apply to Main Backend (Optional)

If you want to mount the generated routes in the main FastAPI app:

```bash
curl -X POST "http://localhost:8000/reverse/apply" \
  -H "Content-Type: application/json" \
  -d '{"api_slug": "stripe"}'
```

This will:
- Mount routes at `/generated/{api_slug}/*`
- Sync the package to `generated_output/{api_slug}/`
- Seed the database with synthesized sample data

Routes will be available at: `http://localhost:8000/generated/stripe/v1/...`

#### Step 6: Run Standalone API (Recommended)

Instead of applying to the main backend, you can run a **completely standalone** version:

```bash
cd generated_output/stripe

# Install dependencies
pip install -r requirements.txt

# Run the standalone API
python main.py
```

The standalone API includes:
- ✅ All generated routes
- ✅ In-memory data storage (no database required)
- ✅ Self-contained FastAPI application
- ✅ Interactive docs at `http://localhost:8000/docs`

**Benefits of standalone:**
- No database setup required
- Completely isolated from the main backend
- Easy to deploy independently
- Perfect for development and testing

See `generated_output/{api_slug}/README_STANDALONE.md` for detailed instructions.

#### Cleanup (Optional)

Remove generated assets:

```bash
curl -X POST "http://localhost:8000/reverse/cleanup" \
  -H "Content-Type: application/json" \
  -d '{"api_slug": "stripe"}'
```

### API Endpoints Summary

**Ingestion:**
- `POST /apis/upload` - Upload and ingest OpenAPI spec
- `GET /apis` - List all registered APIs
- `GET /apis/{api_slug}/components` - List components for an API

**Generation Pipeline:**
- `POST /reverse/plan` - Generate operation plan
- `POST /reverse/generate` - Generate code, tests, and data
- `GET /reverse/preview?api_slug={slug}` - Preview generated assets
- `POST /reverse/apply` - Apply generated routes to main backend
- `POST /reverse/generate_data` - Generate sample data only
- `POST /reverse/cleanup` - Remove generated assets

## Troubleshooting

- Database connection errors: confirm Docker is running and `DATABASE_URL` is exported.
- Postgres not ready: wait a moment or use the psql health check shown above.
- Many components in one spec causing lock errors: ingestion runs DDL in autocommit to reduce lock usage. If needed, start Postgres with more locks:

```bash
docker rm -f deepmock-postgres
docker run --name deepmock-postgres \
  -e POSTGRES_USER=xxxxx \
  -e POSTGRES_PASSWORD=deepmock \
  -e POSTGRES_DB=deepmock \
  -p 5433:5432 \
  -v deepmock_pg:/var/lib/postgresql/data \
  -d postgres:16 -c max_locks_per_transaction=256
```

- CORS issues from the frontend: ensure backend runs on `http://localhost:8000` and the frontend on `http://localhost:3000`.

## Project structure

```
backend/
  main.py            # FastAPI app + routes
  database.py        # SQLAlchemy engine & tables
  ingestion.py       # OpenAPI ingestion → tables + registries
  templates/         # HTML templates (legacy server-rendered UI)
frontend/
  src/app/           # Next.js App Router pages
  src/lib/api.ts     # Frontend fetch helpers for backend routes
```

## Clean up

```bash
docker stop deepmock-postgres
# Remove container (data persists in volume):
docker rm deepmock-postgres
```
