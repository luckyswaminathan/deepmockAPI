# Repository Guidelines

## Project Structure & Module Organization
The backend lives in `backend/`. `main.py` hosts the FastAPI application and uvicorn bootstrap. Runtime dependencies sit in `requirements.txt`, with metadata in `pyproject.toml`. Add automated tests under a top-level `tests/` package; mirror the module layout (`tests/test_main.py`, etc.) so imports stay straightforward.

## Build, Test, and Development Commands
- `python3 -m venv .venv && source .venv/bin/activate`: create and activate a local virtual environment.
- `pip install -r requirements.txt`: install FastAPI, Uvicorn, and standard extras.
- `python main.py`: start the API with auto-reload when invoked from this directory.
- `uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000`: explicit Uvicorn entry point that mirrors production configuration.
- `pytest`: run the automated suite once tests are in place.
Add new CLI helpers to `pyproject.toml` under `[project.scripts]` to keep entry points discoverable.

## Coding Style & Naming Conventions
Follow PEP 8: four-space indents, snake_case functions and modules, PascalCase classes, and UPPER_CASE constants. Prefer explicit type hints on public functions (e.g., `def read_root() -> dict[str, str]:`). Keep FastAPI route handlers slim and move business logic into helper modules as the service grows. Introduce `black` or `ruff` formatting only alongside tooling docs.

## Testing Guidelines
Adopt `pytest` with files named `test_<module>.py` in `/tests`. Use descriptive test names (`test_read_root_returns_status_ok`). When adding FastAPI routes, cover success and failure paths via `fastapi.testclient.TestClient`. Target >90% coverage on new modules and note any intentional gaps in pull requests.

## Commit & Pull Request Guidelines
Current history favors short, imperative subjects (e.g., `init`). Continue that style: start with a verb, keep to ≤72 characters, and add a body when context is not obvious. Pull requests should summarize changes, list validation steps (`pytest`, manual endpoint checks), and link to tracking issues. Include example responses or screenshots when API payloads change.

## Security & Configuration Tips
Do not commit `.venv/`, `.env`, or secrets. Source configuration from environment variables and consider `pydantic-settings` or similar for structured settings as complexity increases. Document new environment variables in the README and keep sample `.env` files updated.

## API Upload Process

1. Create a new branch for the API upload.
2. Add the new API to the `main.py` file.
3. Add the new API to the `tests/test_main.py` file.
4. Run the tests to ensure the new API is working.
5. Push the changes to the remote repository.
6. Create a pull request for the changes.
7. Once the pull request is merged, the new API will be deployed to the remote server.