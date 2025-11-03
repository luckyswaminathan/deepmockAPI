# Standalone Stripe API Mock

This is a standalone, self-contained FastAPI application that mocks the Stripe API. No database or external dependencies required—just FastAPI and uvicorn.

## How This Was Generated

This standalone API was created through the DeepMock pipeline:

1. **Upload** OpenAPI spec → `backend/api/routes/apis.py` (via `/apis/upload`)
2. **Plan** generation → LLM creates operation plan
3. **Generate** code → `backend/reverse/generator.py` generates routes
4. **Apply** → Assets synced here via `backend/reverse/package_manager.py`

The standalone structure (including `main.py` and `runtime.py`) was automatically created during the apply step.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
   Only requires:
   - `fastapi>=0.115.0`
   - `uvicorn[standard]>=0.30.0`

2. **Run the API:**
   ```bash
   python main.py
   ```
   
   Or with uvicorn directly:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

3. **Access the API:**
   - **API**: http://localhost:8000
   - **Interactive docs**: http://localhost:8000/docs
   - **OpenAPI spec**: http://localhost:8000/openapi.json
   - **Health check**: http://localhost:8000/health

## API Endpoints

All Stripe API endpoints are available under `/v1/`. Examples:

- `GET /v1/accounts` - List accounts
- `POST /v1/accounts` - Create account
- `GET /v1/accounts/{account}` - Get account by ID
- `DELETE /v1/accounts/{account}` - Delete account
- `POST /v1/charges` - Create charge
- `GET /v1/charges` - List charges
- etc.

All endpoints from the original OpenAPI spec are available. Check `/docs` for the complete interactive API documentation.

## Data Storage

This mock API uses **in-memory storage** via `runtime.py`. 

**Characteristics:**
- ✅ No database required
- ✅ Data persists during the server session
- ❌ Data resets on server restart
- ✅ Perfect for development/testing
- ✅ Fast and simple

### Seeding Initial Data

To seed initial data, you can:

1. **Modify `runtime.py`** to add data on startup:
   ```python
   def _seed_data():
       _storage["account"] = [
           {"id": "acct_123", "type": "standard", ...},
           ...
       ]
   ```

2. **Use the original data generators** (if available):
   ```python
   from data.generators.generate_components import generate_accounts
   # Use generators to create realistic test data
   ```

3. **POST data via API**:
   ```bash
   curl -X POST http://localhost:8000/v1/accounts \
     -H "Content-Type: application/json" \
     -d '{"id": "acct_123", "type": "standard"}'
   ```

### Persistent Storage (Optional)

To add persistent storage, you can:

1. **Use SQLite** (modify `runtime.py`):
   ```python
   import sqlite3
   # Replace in-memory dict with SQLite operations
   ```

2. **Use JSON file** (modify `runtime.py`):
   ```python
   import json
   # Load/save data to JSON file on startup/shutdown
   ```

3. **Use external database** (modify `runtime.py`):
   ```python
   import psycopg
   # Connect to PostgreSQL/MySQL/etc.
   ```

## Standalone Structure

```
stripe/
├── main.py              # FastAPI app entry point
├── runtime.py           # In-memory data storage
├── requirements.txt     # Minimal dependencies
├── code/
│   ├── routes.py        # Generated route handlers (4000+ lines)
│   └── services.py      # Service layer scaffolding
├── data/
│   ├── generators/      # Data generators
│   └── seeds/           # Sample fixtures
├── tests/               # Test stubs
└── plan/                # Generation plan
```

## Deployment

### Local Development
```bash
python main.py
```

### Production (Docker)
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Cloud Platforms

Works with any platform that supports Python/FastAPI:
- **Vercel**: Use `vercel.json` for serverless
- **Railway**: Deploy directly from Git
- **Fly.io**: Use `fly.toml`
- **Heroku**: Use `Procfile` with `web: uvicorn main:app --host 0.0.0.0 --port $PORT`

## Running as a Module

You can also run it from the parent directory:
```bash
cd generated_output/stripe
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

## Authentication & Auth-Dependent Endpoints

Some endpoints (like `/v1/balance`) depend on authentication context. The generated code provides:

- **`auth.py`** - Mock authentication helpers
- **Account-scoped storage** - Per-account data isolation via `runtime.py`
- **Examples** - See `examples_balance_endpoint.py` for auth handling patterns

**Default Behavior:**
- Optional auth (for development/testing)
- Defaults to mock API key `sk_test_mock_default` if no auth provided
- Supports both Bearer tokens and `Stripe-Api-Key` header

**See `AUTH_GUIDE.md`** for complete documentation on handling auth-dependent endpoints.

## Customization

Customize the generated API by editing:

- **Routes**: `code/routes.py` - Add business logic to handlers
- **Auth**: `auth.py` - Customize authentication logic
- **Storage**: `runtime.py` - Modify data persistence (includes account-scoped ops)
- **Services**: `code/services.py` - Implement service methods
- **CORS**: `main.py` - Adjust allowed origins
- **Docs**: `main.py` - Update title/description

## Troubleshooting

**Port already in use:**
```bash
# Change port in main.py or use uvicorn flag
uvicorn main:app --port 8001
```

**Import errors:**
- Ensure you're in the `generated_output/stripe` directory
- Check that `runtime.py` is in the same directory as `main.py`
- Verify Python path: `python --version` (3.12+)

**CORS issues:**
- Update `allow_origins` in `main.py` if accessing from a different origin

## Related Documentation

- **Main README**: `../../README.md` - Complete pipeline documentation
- **Generated README**: `README.md` - Generated assets overview
- **Backend README**: `../../backend/README.md` - Backend development guide

