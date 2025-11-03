# Standalone Stripe API Mock

This is a standalone, self-contained FastAPI application that mocks the Stripe API.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the API:**
   ```bash
   python main.py
   ```

   Or with uvicorn directly:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

3. **Access the API:**
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - OpenAPI spec: http://localhost:8000/openapi.json

## API Endpoints

All Stripe API endpoints are available under `/v1/`. For example:
- `GET /v1/accounts` - List accounts
- `POST /v1/accounts` - Create account
- `GET /v1/accounts/{account}` - Get account by ID
- etc.

## Data Storage

This mock API uses in-memory storage. All data is stored in memory and will be lost when the server restarts.

To seed initial data, you can modify the `runtime.py` file or add a startup script.

## Standalone Structure

- `main.py` - FastAPI application entry point
- `code/routes.py` - Generated route handlers
- `runtime.py` - In-memory data storage runtime
- `requirements.txt` - Python dependencies

## Running as a Module

You can also run it from the parent directory:
```bash
cd generated_output/stripe
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

