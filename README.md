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
export DATABASE_URL='postgresql+psycopg://lswamina:deepmock@localhost:5433/deepmock'
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

- Upload an OpenAPI spec at `/upload` (JSON or YAML). Optionally provide a friendly API name.
- After a successful upload, see the API listed on the home page `/`.
- Click into an API to view its components and open a component to inspect its properties.

## Troubleshooting

- Database connection errors: confirm Docker is running and `DATABASE_URL` is exported.
- Postgres not ready: wait a moment or use the psql health check shown above.
- Many components in one spec causing lock errors: ingestion runs DDL in autocommit to reduce lock usage. If needed, start Postgres with more locks:

```bash
docker rm -f deepmock-postgres
docker run --name deepmock-postgres \
  -e POSTGRES_USER=lswamina \
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
