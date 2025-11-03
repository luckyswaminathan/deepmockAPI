# Generated assets for stripe

- Generated at: 2025-11-03T21:50:48.015858+00:00
- This directory contains the complete mock API implementation generated from the Stripe OpenAPI spec.

## How This Was Generated

This API was generated through the DeepMock reverse engineering pipeline:

1. **Upload**: OpenAPI spec was uploaded via `POST /apis/upload`
2. **Planning**: LLM-generated plan was created at `backend/reverse/generated/stripe/plan/`
3. **Generation**: Code, tests, and data generators were generated via `POST /reverse/generate`
4. **Sync**: Assets were synced to this directory via `POST /reverse/apply`

See the main `README.md` for the complete pipeline documentation.

## Contents

- `plan/plan.json` — Machine-readable operation plan
- `plan/plan.md` — Human-readable plan documentation
- `plan/route_inventory.json` — Complete route inventory from OpenAPI spec
- `stripe.md` — API routes documentation
- `code/routes.py` — FastAPI route handlers (4288+ lines)
- `code/services.py` — Service layer scaffolding
- `tests/test_routes.py` — Pytest test stubs
- `data/generators/` — Deterministic data generators
- `data/seeds/` — Sample JSON fixtures
- `prompts/` — LLM prompt transcripts

## Running the API

### Option 1: Standalone API (Recommended)

Run this as a completely isolated FastAPI application:

```bash
# Install dependencies (minimal: FastAPI + uvicorn only)
pip install -r requirements.txt

# Run the standalone API
python main.py
```

**Access:**
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- All Stripe endpoints: http://localhost:8000/v1/...

This uses in-memory storage (no database required). See `README_STANDALONE.md` for details.

### Option 2: Mount in Main Backend

If you want to run this within the main DeepMock backend:

```bash
# Apply the generated routes to the main backend
curl -X POST "http://localhost:8000/reverse/apply" \
  -H "Content-Type: application/json" \
  -d '{"api_slug": "stripe"}'
```

Routes will be available at: `http://localhost:8000/generated/stripe/v1/...`

This requires:
- PostgreSQL database (configured via `DATABASE_URL`)
- Main backend server running

## Reviewing Generated Code

1. **Plan**: Review `plan/plan.md` to understand inferred operations
2. **Routes**: Check `code/routes.py` for generated FastAPI handlers
3. **Data**: Inspect `data/seeds/` for sample data structure
4. **Tests**: Review `tests/test_routes.py` for test scaffolding

## Customization

The generated code is meant to be customized:

- **Route handlers**: Edit `code/routes.py` to add business logic
- **Services**: Implement service methods in `code/services.py`
- **Data generators**: Modify `data/generators/` for custom data shapes
- **Standalone runtime**: Edit `runtime.py` to customize storage behavior

## Next Steps

1. Review `plan/plan.md` and `stripe.md` for API documentation
2. Review `code/routes.py` for generated route handlers
3. Run the standalone API: `python main.py`
4. Test endpoints via http://localhost:8000/docs
5. Customize routes and services as needed
6. Add tests in `tests/test_routes.py`