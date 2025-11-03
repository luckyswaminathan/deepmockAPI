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
1. Build the backend image (contains the generator runtime and CLI tools):
   
   ```bash
   docker build -t deepmock-backend:latest backend
   ```

2. Launch a per-API generation job. The helper script provisions an isolated Docker network,
   starts a transient PostgreSQL container, runs the generator image, and cleans everything up:

   ```bash
   python backend/scripts/run_generation_job.py \
     --api-slug stripe \
     --manifest /absolute/path/to/manifest.json
   ```

   - The script uses `reverse-generate --api-slug <slug>` by default; pass a custom command after
     `--` if you need a different entrypoint.
   - All generated records already include `api_slug` columns (`api_registry`, `component_registry`,
     and `generated_records` tables), so a shared PostgreSQL instance can host multiple API slugs
     without data collisions.
   - To reuse an external database instead of the transient PostgreSQL container, provide
     `--shared-database-url postgresql+psycopg://user:pass@host:5432/dbname`.

OpenAPI Workflow
----------------
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

Visit
-----
- Dashboard & health: `http://localhost:8000/`
- Interactive docs (Swagger): `http://localhost:8000/docs`
- Alternative docs (ReDoc): `http://localhost:8000/redoc`


