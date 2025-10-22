# Mock Server

Single-process mock server that synthesises responses from the provided OpenAPI specification. The server builds a dependency graph across component schemas, composes payloads in topological order, and validates every response at runtime.

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Set optional query parameters per request:

- `latency_ms`: Artificial latency in milliseconds.
- `error_code`: Force a particular error response when defined in the spec.
- `seed`: Control Faker's deterministic output.

## Testing

```bash
pytest tests/unit
pytest tests/contract
```

Contract tests are powered by [schemathesis](https://schemathesis.readthedocs.io/).

## Tooling

- Runtime validation via `jsonschema`.
- OpenAPI linting with `npx @stoplight/spectral-cli lint openapi.yaml`.
- Docker image provided (`Dockerfile`) for containerised execution.
