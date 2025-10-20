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
