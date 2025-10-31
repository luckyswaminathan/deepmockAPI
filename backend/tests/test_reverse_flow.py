import importlib
import json
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True, scope="module")
def add_backend_to_syspath() -> None:
    backend_dir = Path(__file__).resolve().parents[1]
    if str(backend_dir) not in sys.path:
        sys.path.insert(0, str(backend_dir))


@pytest.fixture
def client(tmp_path, monkeypatch) -> TestClient:
    root = Path(__file__).resolve().parents[1]
    backend_dir = root / "backend"
    if str(backend_dir) not in sys.path:
        sys.path.insert(0, str(backend_dir))

    db_path = tmp_path / "test.db"
    monkeypatch.setenv("_DATABASE_URL", f"sqlite:///{db_path}")

    import database

    database.get_database_url.cache_clear()
    database.get_engine.cache_clear()

    import main

    importlib.reload(main)

    with TestClient(main.app) as test_client:
        yield test_client


def _build_sample_spec() -> dict:
    return {
        "openapi": "3.0.0",
        "info": {"title": "Sample API", "version": "1.0.0"},
        "paths": {
            "/orders": {
                "get": {
                    "summary": "List orders",
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/OrderList"}
                                }
                            }
                        }
                    },
                }
            },
            "/orders/{orderId}": {
                "get": {
                    "summary": "Get order",
                    "parameters": [
                        {
                            "name": "orderId",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string"},
                        }
                    ],
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Order"}
                                }
                            }
                        }
                    },
                }
            },
        },
        "components": {
            "schemas": {
                "Order": {
                    "type": "object",
                    "required": ["id"],
                    "properties": {
                        "id": {"type": "string"},
                        "status": {"type": "string"},
                    },
                },
                "OrderList": {
                    "type": "object",
                    "properties": {
                        "items": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/Order"},
                        }
                    },
                },
            }
        },
    }


def test_reverse_engineering_flow(client: TestClient) -> None:
    spec = _build_sample_spec()
    spec_payload = json.dumps(spec)

    upload_response = client.post(
        "/apis/upload",
        files={"spec_file": ("spec.json", spec_payload, "application/json")},
    )
    assert upload_response.status_code == 200
    api_slug = upload_response.json()["api_slug"]

    reverse_ingest_response = client.post(
        "/reverse/ingest_spec",
        json={"spec": spec, "api_name": "Sample API"},
    )
    assert reverse_ingest_response.status_code == 200
    ingest_data = reverse_ingest_response.json()
    assert ingest_data["api_slug"] == api_slug
    assert ingest_data["route_count"] == 2

    plan_response = client.post("/reverse/plan", json={"api_slug": api_slug})
    assert plan_response.status_code == 200
    content_type = plan_response.headers.get("content-type", "")
    assert content_type.startswith("text/markdown"), "Plan response should be Markdown"
    plan_markdown = plan_response.text
    assert "Reverse Engineering Plan" in plan_markdown
    assert "GET /orders" in plan_markdown

    plan_md_path = (
        Path(__file__).resolve().parents[1]
        / "reverse"
        / "generated"
        / api_slug
        / "plan"
        / "plan.md"
    )
    assert plan_md_path.exists(), "Expected plan markdown file to be written"

    generate_response = client.post("/reverse/generate", json={"api_slug": api_slug})
    assert generate_response.status_code == 200
    report = generate_response.json()
    assert any(file.endswith("routes.py") for file in report["files_written"])

    preview_response = client.get("/reverse/preview", params={"api_slug": api_slug})
    assert preview_response.status_code == 200
    preview_data = preview_response.json()
    assert preview_data["files"], "Preview should list generated files"

    data_response = client.post("/reverse/generate_data", json={"api_slug": api_slug})
    assert data_response.status_code == 200
    dataset = data_response.json()["dataset"]
    assert dataset, "Expected synthesized dataset"

    apply_response = client.post("/reverse/apply", json={"api_slug": api_slug})
    assert apply_response.status_code == 200
    assert apply_response.json()["applied"] is True

    package_dir = Path(__file__).resolve().parents[1] / "generated_apis" / api_slug
    assert package_dir.exists()
    module = importlib.import_module(f"generated_apis.{api_slug}.routes")
    assert hasattr(module, "router")

    list_response = client.get(f"/generated/{api_slug}/orders")
    assert list_response.status_code == 200
    list_payload = list_response.json()
    assert isinstance(list_payload, list) and list_payload, "Expected generated records in live endpoint"

    record_id = list_payload[0]["id"]
    detail_response = client.get(f"/generated/{api_slug}/orders/{record_id}")
    assert detail_response.status_code == 200
    assert detail_response.json()["id"] == record_id

    cleanup_response = client.post("/reverse/cleanup", json={"api_slug": api_slug})
    assert cleanup_response.status_code == 200
    assert cleanup_response.json()["removed"] is True
    assert not package_dir.exists()
