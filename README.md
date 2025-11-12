# DeepMock API – Local Development

This repository contains a FastAPI backend (with background generation jobs) and a Next.js frontend. The whole stack now runs by starting the Docker Compose services from the repo root and then launching the frontend dev server.

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

## Useful Notes
- Backend CORS already allows `http://localhost:3000`.
- All generated data is stored inside `backend/deepmock.db` (SQLite) and mirrored to `generated_output/`.
- Use `_DATABASE_URL`/`DATABASE_URL` to point to a different SQLite or Postgres instance if desired.

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
