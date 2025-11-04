# DeepMock API – Local Development

This repository contains a FastAPI backend and a Next.js frontend. Follow the steps below to run everything locally.

## Prerequisites

- Docker
- Python 3.12+
- Node.js 18+ and npm
- Optional: `psql` CLI (for database health checks)

## Setup & Run

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

**Notes:**
- Core tables are created automatically on startup.
- CORS is enabled for `http://localhost:3000`.

### 3. Upload OpenAPI Specification

**Option A: Via API (curl)**

```bash
curl -X POST "http://localhost:8000/apis/upload" \
  -F "spec_file=@path/to/your/openapi.json" \
  -F "api_name=Your API Name"
```

**Option B: Via Frontend**

In a separate terminal:

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

## Additional Information

### Basic Workflow (Component Inspection)

- Upload an OpenAPI spec at `/upload` (JSON or YAML). Optionally provide a friendly API name.
- After a successful upload, see the API listed on the home page `/`.
- Click into an API to view its components and open a component to inspect its properties.

### Alternative: Generate via API Endpoints

Instead of using the Docker CLI, you can also generate via API endpoints:

**Review Plan (Optional):**
```bash
# Replace {api_slug} with your API slug
curl -X POST "http://localhost:8000/reverse/plan" \
  -H "Content-Type: application/json" \
  -d '{"api_slug": "{api_slug}"}'
```

**Generate Code:**
```bash
# Replace {api_slug} with your API slug
curl -X POST "http://localhost:8000/reverse/generate" \
  -H "Content-Type: application/json" \
  -d '{"api_slug": "{api_slug}"}'
```

**Run Standalone API:**
```bash
# Replace {api_slug} with your API slug
cd generated_output/{api_slug}
pip install -r requirements.txt
python main.py
```

### Standalone API Output

After generation, your standalone API will be available at `generated_output/{api_slug}/` with:
- ✅ All generated routes
- ✅ In-memory data storage (no database required)
- ✅ Self-contained FastAPI application
- ✅ Interactive docs at `http://localhost:8000/docs`

See `generated_output/{api_slug}/README_STANDALONE.md` for detailed instructions.

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

- **Database connection errors**: Confirm Docker is running and `DATABASE_URL` is exported.
- **Postgres not ready**: Wait a moment after starting the container.
- **Many components causing lock errors**: Start Postgres with more locks:

```bash
docker rm -f deepmock-postgres
docker run --name deepmock-postgres \
  -e POSTGRES_USER=deepmock \
  -e POSTGRES_PASSWORD=deepmock \
  -e POSTGRES_DB=deepmock \
  -p 5432:5432 \
  -v deepmock_pg:/var/lib/postgresql/data \
  -d postgres:16 -c max_locks_per_transaction=256
```

- **CORS issues**: Ensure backend runs on `http://localhost:8000` and frontend on `http://localhost:3000`.

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
