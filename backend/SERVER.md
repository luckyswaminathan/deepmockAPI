## PRD: API Reverse-Engineering and Code Generation Service

### 1) Overview
Given an API specification and a component registry stored in our DB (including the component dependency graph), the system infers the database operations required for each route, then generates the code necessary to perform those operations. It also synthesizes sample data by walking the component graph from leaves upward. Outputs are written to a standalone side folder that can be inspected, tested, and optionally wired into the running service.

### 2) Goals
- **Reverse-engineer DB operations from API routes**: For each route in the input API spec, infer CRUD ops, joins, filters, and constraints against the component registry.
- **Generate implementation code**: Produce repositories, services, and route handlers implementing the inferred operations via templates.
- **Autogenerate sample data**: Identify leaf components and generate base data, then propagate relationships to produce coherent fixture datasets (deterministic and reproducible).
- **Ship as a general generator**: Emit outputs into a new, versioned side folder without mutating existing code unless explicitly applied.

### 3) Non-Goals
- Execute schema migrations or alter existing DB schema automatically.
- Guarantee perfect LLM inference; instead, validate and surface a human-reviewable plan with guardrails and fallbacks.
- Hot-plug generated routes into production without manual review.

### 4) Primary Users
- Internal developers who want to bootstrap server-side implementations from an API spec + component graph.

### 5) Inputs
- **API Spec**: OpenAPI (JSON/YAML) or a structured route list `{ method, path, requestSchema, responseSchema }`.
- **Component Registry** (in DB): Tables, fields, primary/foreign keys, constraints, and a directed acyclic component graph describing dependencies.
- **Configuration**: Output directory, target language/runtime (Python/FastAPI), LLM provider/config, generation options (tests, data volume, dry-run).

### 6) Outputs
- **Side Folder** under `generated/<api_slug>/` containing:
  - `plan/`: Machine-readable plan (`plan.json`) of inferred DB operations per route.
  - `code/`: Generated `models/`, `repositories/`, `services/`, `routes/` with typed functions and FastAPI handlers.
  - `tests/`: Pytest stubs validating endpoints and repository behaviors.
  - `data/`: Deterministic data generators and sample JSON/CSV fixtures.
  - `prompts/`: Prompt transcripts for reproducibility/debugging.
  - `README.md`: How to run, test, and apply.

### 7) High-Level Architecture
- **Planner**: Consumes the API spec and component graph to produce a normalized route inventory and an operation plan using an LLM with schema-aware prompts.
- **Validator**: Checks inferred operations against the registry/schema (FKs, nullability, indices) and flags mismatches.
- **Generator**: Renders repositories/services/routes/tests via templates (Jinja2) using the validated plan.
- **Data Synthesizer**: Uses leaves of the graph to create base records, then expands up edges to satisfy relationships; emits deterministic seeds.
- **Orchestrator API (FastAPI)**: Endpoints to ingest, plan, generate, preview, and apply outputs.

### 8) Orchestrator Endpoints (Backend)
- `POST /reverse/ingest_spec` → Store/normalize API spec; return `api_slug` and route inventory.
- `POST /reverse/plan` → Generate LLM-backed operation plan; persist under `generated/<api_slug>/plan/plan.json`.
- `POST /reverse/generate` → Emit code, tests, and data generators to `generated/<api_slug>/code|tests|data`.
- `GET /reverse/preview` → Zip/HTML preview of generated assets; return diffs and validation warnings.
- `POST /reverse/apply` → Optional copy of selected assets into the main backend (guarded, off by default).
- `POST /reverse/cleanup` → Remove generated folder(s) for an `api_slug`.

### 9) Component Registry & Graph (Conceptual Model)
- `components`:
  - `id` (pk), `name`, `table_name`, `fields` (JSON), `primary_key`, `unique_constraints` (list), `indexes` (list)
- `relationships`:
  - `from_component_id`, `to_component_id`, `type` (`one_to_many`, `many_to_many`, etc.), `fk_field`, `on_delete`
- `graph`:
  - DAG of components; leaves are nodes with out-degree 0. Leaves seed base data.

### 10) Planning Workflow
1) Normalize the API spec → `route_inventory` of `{method, path, request, response}`.
2) For each route, infer the target component(s) from `path` and `schema` names.
3) Use LLM to produce an operation plan with:
   - Operation type(s) (create/read/update/delete, transactional grouping)
   - Component(s) touched, join path(s), filters, pagination
   - Validation and error cases
   - Expected response shape ↔ component fields mapping
4) Validate plan against registry; record errors/warnings.
5) Emit `plan.json` for review; require “green” status or allow generate with warnings.

Example plan excerpt:
```json
{
  "routes": [
    {
      "method": "GET",
      "path": "/orders/{orderId}",
      "operations": [
        {
          "type": "read_one",
          "component": "Order",
          "filters": [{"field": "id", "op": "eq", "valueFrom": "path.orderId"}],
          "joins": [
            {"component": "OrderItem", "on": "Order.id = OrderItem.order_id"},
            {"component": "Product", "on": "OrderItem.product_id = Product.id"}
          ],
          "responseMapping": "Order -> OrderDTO"
        }
      ]
    }
  ],
  "validation": {"errors": [], "warnings": ["Missing index on OrderItem.order_id"]}
}
```

### 11) Code Generation Workflow
- Templates generate:
  - **Repositories**: CRUD with composable filters and joins using SQLAlchemy.
  - **Services**: Business logic orchestration; type-annotated.
  - **Routes**: FastAPI handlers with Pydantic models.
  - **Tests**: `TestClient` success/failure cases; repository unit tests with an in-memory DB or sqlite.

Folder layout (example):
```text
generated/
  <api_slug>/
    plan/
      plan.json
    code/
      models/
      repositories/
      services/
      routes/
      __init__.py
    tests/
      test_routes.py
      test_repositories.py
    data/
      generators/
        generate_components.py
      seeds/
        sample.json
    prompts/
      plan_prompt.txt
      validation_prompt.txt
    README.md
```

### 12) Data Generation
- Identify graph leaves; generate N base records per leaf using deterministic factories (seeded faker).
- Traverse edges upward to satisfy FKs; cardinality respects `one_to_many`, `many_to_many` via junctions.
- Emit:
  - `generators/generate_components.py` with `generate(count_by_component: dict[str,int], seed:int) -> dict[str,list[dict]]`.
  - `seeds/sample.json` as a compact sample corpus.
- Provide a `POST /reverse/generate_data` endpoint to produce ad-hoc datasets from a request payload.

### 13) LLM Strategy & Guardrails
- Abstract provider via `llm.py`; default to environment-configured model.
- Constrain prompts with the registry schema (tables, fields, relationships) and response contracts.
- Toolformer-like style: require the model to emit a strict JSON plan; reject on schema violations.
- Keep temperature low; retry with reduced scope when validation fails.
- Persist prompts/responses for audit and reproducibility.

### 14) Configuration
- Env vars: `GEN_OUTPUT_DIR`, `GEN_MODEL`, `GEN_TEMPERATURE`, `GEN_MAX_TOKENS`, `GEN_APPLY_ENABLED`.
- CLI wrappers in `pyproject.toml` under `[project.scripts]` for local runs.

### 15) Success Metrics & Acceptance Criteria
- >= 90% of routes produce a valid plan without manual edits on first pass for well-formed specs.
- Generated code passes `pytest` and imports cleanly under `uvicorn` in isolation.
- Data generator yields referentially consistent datasets with stable seeds.
- Human review time per medium API (<30 routes) ≤ 1 hour on average.

### 16) Risks & Mitigations
- **Hallucinated fields/joins**: Strict schema-in-the-loop validation; fail closed.
- **Complex join paths**: Limit join depth; suggest indices in warnings.
- **Schema drift**: Versioned registry snapshots embedded in `plan/`.
- **Security**: Do not auto-apply to production; sanitize prompts; avoid PII in logs.

### 17) Phased Delivery (Milestones)
- M1: Spec ingestion + route inventory + basic UI preview.
- M2: Component graph fetch + schema normalizer.
- M3: LLM planning + validator with JSON schema.
- M4: Code generator for repos/services/routes + tests.
- M5: Data synthesizer (leaves → full graph) + endpoints.
- M6: Apply/preview UX + CLI + docs.
- M7: Hardening, coverage >90% on generator modules.

### 18) Open Questions
- Should we support multi-tenant schemas out of the box?
- Minimum Python version and ORM (SQLAlchemy 2.x assumed)?
- Strategy for migrations when plan suggests new indices?

### 19) Developer Notes
- Keep FastAPI handlers thin; centralize logic in `services/`.
- Match PEP 8 and add explicit type hints for public APIs.
- Record all LLM IO under `prompts/` to aid debugging.

