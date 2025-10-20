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
3. The backend parses `components.schemas` and creates one PostgreSQL table per component
   (named `<api-slug>_<component-name>`). Properties (field name, type, description, required, etc.)
   are stored as rows in the generated table.
4. Browse the ingested APIs and their component tables directly from the dashboard. You can also
   query the REST endpoints:
   - `POST /apis/upload` – ingest a specification.
   - `GET /apis` – list registered APIs.
   - `GET /apis/{api_slug}/components` – list component tables for an API.
   - `GET /apis/{api_slug}/components/{component_name}` – view properties for a component.

Visit
-----
- Dashboard & health: `http://localhost:8000/`
- Interactive docs (Swagger): `http://localhost:8000/docs`
- Alternative docs (ReDoc): `http://localhost:8000/redoc`
