from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Optional, Tuple

from reverse import data_synthesizer
from reverse.models import GenerationReport, OperationPlan, ReversePlan, RoutePlan
from reverse.planner import build_plan, load_route_inventory
from reverse.storage import api_root, list_generated_files, write_json, write_text
from reverse.utils import ensure_dir, extract_path_params, split_path_components


def ensure_plan(api_slug: str, plan: Optional[ReversePlan] = None) -> ReversePlan:
    if plan is not None:
        return plan
    route_inventory = load_route_inventory(api_slug)
    return build_plan(api_slug, route_inventory=route_inventory)


def generate(plan: ReversePlan | None, api_slug: str) -> GenerationReport:
    resolved_plan = ensure_plan(api_slug, plan)
    root = api_root(api_slug)
    ensure_dir(root)

    files_written: list[str] = []
    files_written.extend(_write_readme(root, resolved_plan))
    files_written.extend(_write_code(root, resolved_plan))
    files_written.extend(_write_tests(root, resolved_plan))
    files_written.extend(_write_data(root, resolved_plan))
    files_written.extend(_write_prompts(root, resolved_plan))
    files_written.extend(_write_routes_documentation(root, resolved_plan))

    # Re-write plan.json to ensure latest timestamp.
    write_json(root / "plan" / "plan.json", resolved_plan.dict())

    # Automatically generate data for ALL components after code generation
    # This uses graph-based generation to create data for every component
    try:
        from reverse import runtime
        
        import sys
        print(f"[generator] Starting data generation for {api_slug}...", file=sys.stderr)
        
        dataset = data_synthesizer.synthesize_all_components(
            api_slug,
            count_per_component=None,  # Uses default of 3 per component
            store_in_db=False,  # We'll use replace_dataset to store all at once
        )
        
        print(f"[generator] Generated dataset with {len(dataset)} components", file=sys.stderr)
        
        # Store all generated records in GeneratedRecord database table
        if dataset:
            total_records = sum(len(records) for records in dataset.values())
            print(f"[generator] Storing {total_records} total records in database...", file=sys.stderr)
            runtime.replace_dataset(api_slug, dataset)
            print(f"[generator] Successfully stored {total_records} records for {api_slug}", file=sys.stderr)
        else:
            print(f"[generator] WARNING: Dataset is empty for {api_slug}", file=sys.stderr)
    except ValueError as e:
        # API not found or has no components - skip data generation gracefully
        import sys
        error_msg = str(e).lower()
        if "not found" in error_msg or "no components" in error_msg:
            print(f"[generator] SKIP: {e}", file=sys.stderr)
            print(f"[generator] Hint: Upload OpenAPI spec via /apis/upload before generating data.", file=sys.stderr)
        else:
            # Re-raise if it's a different ValueError
            raise
    except Exception as e:
        # Don't fail code generation if data generation fails
        # But log the full error for debugging
        import sys
        import traceback
        print(f"[generator] ERROR: Data generation failed for {api_slug}: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)

    # Automatically sync standalone API files (main.py, runtime.py, requirements.txt)
    # This creates a complete standalone FastAPI application in generated_output/{api_slug}/
    # that can be run independently without the main backend
    import sys
    try:
        from reverse import package_manager
        print(f"[generator] Starting sync of standalone API for {api_slug}...", file=sys.stderr)
        standalone_path = package_manager.sync_standalone_api(api_slug)
        print(f"[generator] ✓ Synced standalone API to {standalone_path}", file=sys.stderr)
        print(f"[generator] ✓ Created: main.py, runtime.py, requirements.txt", file=sys.stderr)
    except FileNotFoundError as e:
        # This happens if code hasn't been generated yet - that's ok, we just generated it
        print(f"[generator] NOTE: Standalone sync skipped - {e}", file=sys.stderr)
        print(f"[generator] Run /reverse/apply to create standalone files", file=sys.stderr)
    except Exception as e:
        # Don't fail generation if standalone sync fails, but log the error clearly
        import traceback
        print(f"[generator] ERROR: Failed to sync standalone API for {api_slug}: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        print(f"[generator] Generation completed, but standalone files may be missing.", file=sys.stderr)

    return GenerationReport(
        api_slug=resolved_plan.api_slug,
        output_dir=str(root),
        files_written=sorted(dict.fromkeys(files_written)),
    )


def _write_readme(root: Path, plan: ReversePlan) -> list[str]:
    readme = root / "README.md"
    content = "\n".join(
        [
            f"# Generated assets for {plan.api_slug}",
            "",
            f"- Generated at: {plan.generated_at.isoformat()}",
            "- Copy assets manually after review.",
            "",
            "## Contents",
            "- `plan/plan.json` — machine-readable plan.",
            "- `plan/plan.md` — human-readable plan documentation.",
            f"- `{plan.api_slug}.md` — API routes documentation.",
            "- `code/` — FastAPI router stubs.",
            "- `tests/` — pytest scaffolding.",
            "- `data/` — deterministic data generators and seeds.",
            "- `prompts/` — prompt transcripts placeholders.",
            "",
            "## Next steps",
            f"1. Review `plan/plan.md` and `{plan.api_slug}.md` for API documentation.",
            "2. Review `plan/plan.json` for machine-readable plan details.",
            "3. Flesh out generated route handlers and services.",
            "4. Run `pytest` against generated tests once implemented.",
        ]
    )
    write_text(readme, content)
    return [str(readme.relative_to(root))]


def _write_code(root: Path, plan: ReversePlan) -> list[str]:
    code_dir = root / "code"
    ensure_dir(code_dir)
    files: list[str] = []

    routes_path = code_dir / "routes.py"
    write_text(routes_path, _render_routes_module(plan))
    files.append(str(routes_path.relative_to(root)))

    services_path = code_dir / "services.py"
    write_text(services_path, _render_services_module())
    files.append(str(services_path.relative_to(root)))

    init_path = code_dir / "__init__.py"
    write_text(init_path, "from .routes import router\n\n__all__ = [\"router\"]\n")
    files.append(str(init_path.relative_to(root)))

    return files


def _render_routes_module(plan: ReversePlan) -> str:
    routes = plan.routes
    lines = [
        "from __future__ import annotations",
        "",
        "from typing import Any, Dict",
        "",
        "from fastapi import APIRouter, HTTPException",
        "",
        "# Import local runtime module from parent directory",
        "import sys",
        "from pathlib import Path",
        "",
        "# Add parent directory to Python path to import runtime",
        "parent_dir = str(Path(__file__).parent.parent)",
        "if parent_dir not in sys.path:",
        "    sys.path.insert(0, parent_dir)",
        "",
        "import runtime as generated_runtime",
        "",
        f'API_SLUG = "{plan.api_slug}"',
        "",
        "router = APIRouter()",
        "",
    ]

    for route in routes:
        if not route.operations:
            comment = f"# TODO: No operations inferred for {route.method} {route.path}"
            lines.append(comment)
            continue
        operation = route.operations[0]
        func_name = _make_function_name(route)
        method = route.method.lower()
        path = route.path
        params = _build_function_params(route, operation)
        doc_lines = [
            f'"""Autogenerated stub for {route.method} {route.path}.',
        ]
        if route.component:
            doc_lines.append(f"Target component: {route.component}.")
        else:
            print(route.path)
        doc_lines.append('"""')
        signature = ", ".join(["*"] + params) if params else ""

        lines.extend(
            [
                f"@router.{method}(\"{path}\")",
                f"async def {func_name}({signature}) -> Any:" if signature else f"async def {func_name}() -> Any:",
            ]
        )
        lines.extend([f"    {line}" for line in doc_lines])
        lines.extend(_render_operation_body(route, operation))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _build_function_params(route: RoutePlan, operation: OperationPlan) -> list[str]:
    params: list[str] = []
    for param in extract_path_params(route.path):
        params.append(f"{param}: str")
    if operation.type in {"create", "update", "update_partial"}:
        params.append("payload: Dict[str, Any]")
    return params


def _make_function_name(route: RoutePlan) -> str:
    components = split_path_components(route.path)
    suffix = "_".join(components) if components else "root"
    # Sanitize invalid Python identifier characters
    # Replace dashes, dots, and other special chars with underscores
    suffix = suffix.replace("-", "_").replace(".", "_").replace("/", "_")
    # Remove any consecutive underscores and leading/trailing underscores
    while "__" in suffix:
        suffix = suffix.replace("__", "_")
    suffix = suffix.strip("_")
    # Ensure it starts with a letter or underscore (Python identifier requirement)
    if suffix and not (suffix[0].isalpha() or suffix[0] == "_"):
        suffix = f"_{suffix}"
    method = route.method.lower()
    return f"{method}_{suffix}" if suffix else method


def _render_services_module() -> str:
    return "\n".join(
        [
            "from __future__ import annotations",
            "",
            "from typing import Any",
            "",
            "class GeneratedService:",
            "    \"\"\"Service stub generated from the reverse-engineering pipeline.\"\"\"",
            "",
            "    def execute(self, component: str, payload: dict[str, Any]) -> Any:",
            "        raise NotImplementedError(\"Implement service orchestration logic here.\")",
            "",
        ]
    )


def _write_tests(root: Path, plan: ReversePlan) -> list[str]:
    tests_dir = root / "tests"
    ensure_dir(tests_dir)
    routes_path = tests_dir / "test_routes.py"
    route_count = sum(1 for route in plan.routes if route.operations)
    content = "\n".join(
        [
            "import pytest",
            "",
            "",
            "def test_stub_generated_routes() -> None:",
            f"    assert {route_count} >= 0",
            "",
        ]
    )
    write_text(routes_path, content)
    return [str(routes_path.relative_to(root))]


def _write_data(root: Path, plan: ReversePlan) -> list[str]:
    data_dir = root / "data"
    ensure_dir(data_dir)
    generators_dir = data_dir / "generators"
    ensure_dir(generators_dir)
    seeds_dir = data_dir / "seeds"
    ensure_dir(seeds_dir)

    generator_path = generators_dir / "generate_components.py"
    write_text(generator_path, _render_data_generator())

    seed_path = seeds_dir / "sample.json"
    dataset = data_synthesizer.synthesize(plan)
    payload = {
        "api_slug": plan.api_slug,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "dataset": dataset,
    }
    write_text(seed_path, json.dumps(payload, indent=2) + "\n")

    return [
        str(generator_path.relative_to(root)),
        str(seed_path.relative_to(root)),
    ]


def _render_data_generator() -> str:
    return "\n".join(
        [
            "from __future__ import annotations",
            "",
            "from typing import Any, Dict",
            "",
            "def generate_components(count_by_component: Dict[str, int], seed: int = 1337) -> Dict[str, list[dict[str, Any]]]:",
            '    """Deterministic sample data generator stub."""',
            "    return {name: [{} for _ in range(count)] for name, count in count_by_component.items()}",
            "",
        ]
    )


def _render_operation_body(route: RoutePlan, operation: OperationPlan) -> list[str]:
    component = operation.component or route.component
    if route.component == "error":
        print(route.path)
    if not component:
        return [
            '    raise HTTPException(status_code=501, detail="Generated route missing component mapping.")'
        ]

    if operation.type == "read_many":
        return [
            f'    records = generated_runtime.fetch_component_records(API_SLUG, "{component}")',
            "    return records",
        ]

    if operation.type == "read_one":
        field, param = _select_primary_filter(route, operation)
        if not param:
            return [
                '    raise HTTPException(status_code=501, detail="Unable to determine identifier for read operation.")'
            ]
        return [
            f'    record = generated_runtime.fetch_component_record(API_SLUG, "{component}", "{field}", {param})',
            "    if record is None:",
            '        raise HTTPException(status_code=404, detail="Record not found.")',
            "    return record",
        ]

    if operation.type == "create":
        prelude: list[str] = []
        # Inject all path params into payload for owner/resource scoping
        for p in extract_path_params(route.path):
            prelude.append(f'    payload["{p}"] = {p}')
        # Ensure stable id using the primary identifier (last path param if present)
        path_params = extract_path_params(route.path)
        if path_params:
            primary_param = path_params[-1]
            prelude.append(f'    payload["id"] = {primary_param}')
            prelude.append(f'    payload["record_key"] = {primary_param}')
        return prelude + [
            f'    created = generated_runtime.insert_component_record(API_SLUG, "{component}", payload)',
            "    return created",
        ]

    if operation.type in {"update", "update_partial"}:
        field, param = _select_primary_filter(route, operation)
        if not param:
            return [
                '    raise HTTPException(status_code=501, detail="Unable to determine identifier for update operation.")'
            ]
        prelude: list[str] = []
        # Inject all path params into payload for owner/resource scoping
        for p in extract_path_params(route.path):
            prelude.append(f'    payload["{p}"] = {p}')
        # Ensure stable id using the selected identifier and align record_key for upsert
        prelude.append(f'    payload["id"] = {param}')
        prelude.append(f'    payload["record_key"] = {param}')
        # Perform upsert via insert_component_record
        return prelude + [
            f'    updated = generated_runtime.insert_component_record(API_SLUG, "{component}", payload)',
            "    return updated",
        ]

    if operation.type == "delete":
        field, param = _select_primary_filter(route, operation)
        if not param:
            return [
                '    raise HTTPException(status_code=501, detail="Unable to determine identifier for delete operation.")'
            ]
        return [
            f'    removed = generated_runtime.delete_component_record(API_SLUG, "{component}", "{field}", {param})',
            "    if not removed:",
            '        raise HTTPException(status_code=404, detail="Record not found.")',
            "    return {'deleted': True}",
        ]

    return [
        f'    raise HTTPException(status_code=501, detail="Unsupported operation type: {operation.type}.")'
    ]


def _select_primary_filter(route: RoutePlan, operation: OperationPlan) -> Tuple[str, Optional[str]]:
    path_params = extract_path_params(route.path)
    if not path_params:
        return ("id", None)
    
    # Always treat the LAST path parameter as the canonical record identifier
    # regardless of its name (e.g., "account", "charge", etc.).
    primary_param = path_params[-1]
    return "id", primary_param


def _write_prompts(root: Path, plan: ReversePlan) -> list[str]:
    prompts_dir = root / "prompts"
    ensure_dir(prompts_dir)
    plan_prompt = prompts_dir / "plan_prompt.txt"
    validation_prompt = prompts_dir / "validation_prompt.txt"
    write_text(
        plan_prompt,
        "\n".join(
            [
                "## Plan prompt placeholder",
                f"API slug: {plan.api_slug}",
                f"Generated at: {plan.generated_at.isoformat()}",
            ]
        ),
    )
    write_text(
        validation_prompt,
        "\n".join(
            [
                "## Validation prompt placeholder",
                f"Errors: {len(plan.validation.errors)}",
                f"Warnings: {len(plan.validation.warnings)}",
            ]
        ),
    )
    return [
        str(plan_prompt.relative_to(root)),
        str(validation_prompt.relative_to(root)),
    ]


def _write_routes_documentation(root: Path, plan: ReversePlan) -> list[str]:
    """Generate markdown documentation for all generated routes."""
    doc_path = root / f"{plan.api_slug}.md"
    content = _render_routes_documentation(plan)
    write_text(doc_path, content)
    return [str(doc_path.relative_to(root))]


def _render_routes_documentation(plan: ReversePlan) -> str:
    """Render markdown documentation for generated API routes."""
    lines: list[str] = []
    lines.append(f"# Generated API Routes for `{plan.api_slug}`")
    lines.append("")
    lines.append(f"**Generated at:** {plan.generated_at.isoformat()}")
    lines.append("")
    lines.append("This document describes all generated API routes and their operations.")
    lines.append("")

    if plan.validation.errors or plan.validation.warnings:
        lines.append("## Validation Status")
        if plan.validation.errors:
            lines.append("### Errors")
            for error in plan.validation.errors:
                lines.append(f"- ⚠️ {error}")
            lines.append("")
        if plan.validation.warnings:
            lines.append("### Warnings")
            for warning in plan.validation.warnings:
                lines.append(f"- ⚠️ {warning}")
            lines.append("")

    # Group routes by component
    component_routes: dict[str | None, list[RoutePlan]] = defaultdict(list)
    for route in plan.routes:
        component_routes[route.component].append(route)

    lines.append("## Routes by Component")
    lines.append("")

    for component in sorted(component_routes.keys(), key=lambda x: x or "zzz_unmapped"):
        if component:
            lines.append(f"### Component: `{component}`")
        else:
            lines.append("### Unmapped Routes")
        lines.append("")

        routes = component_routes[component]
        for route in sorted(routes, key=lambda r: (r.method, r.path)):
            lines.append(f"#### `{route.method} {route.path}`")
            
            if route.summary:
                lines.append(f"**Summary:** {route.summary}")
            
            lines.append(f"**Status:** {route.status}")
            lines.append("")

            if route.operations:
                lines.append("**Operations:**")
                for operation in route.operations:
                    lines.append(f"- **{operation.type}**")
                    if operation.component:
                        lines.append(f"  - Component: `{operation.component}`")
                    
                    if operation.filters:
                        lines.append("  - Filters:")
                        for filt in operation.filters:
                            lines.append(f"    - `{filt.field}` {filt.operator} `{filt.value_source}`")
                    
                    if operation.notes:
                        lines.append("  - Notes:")
                        for note in operation.notes:
                            lines.append(f"    - {note}")
            else:
                lines.append("**Operations:** None")
            
            if route.warnings:
                lines.append("**Warnings:**")
                for warning in route.warnings:
                    lines.append(f"- {warning}")
            
            lines.append("")

    # Add route summary table
    lines.append("## Route Summary")
    lines.append("")
    lines.append("| Method | Path | Component | Status | Operations |")
    lines.append("|--------|------|-----------|--------|------------|")
    
    for route in sorted(plan.routes, key=lambda r: (r.method, r.path)):
        component = route.component or "Unmapped"
        operations = ", ".join([op.type for op in route.operations]) if route.operations else "None"
        lines.append(f"| {route.method} | `{route.path}` | {component} | {route.status} | {operations} |")
    
    lines.append("")

    return "\n".join(lines)
