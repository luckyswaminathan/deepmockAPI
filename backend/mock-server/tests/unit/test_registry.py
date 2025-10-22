import pytest

from app.registry import SchemaRegistry, build_schema_graph, topo_order


def test_build_schema_graph_and_topo_order():
    spec = {
        "components": {
            "schemas": {
                "Parent": {
                    "type": "object",
                    "properties": {
                        "child": {"$ref": "#/components/schemas/Child"},
                        "name": {"type": "string"},
                    },
                },
                "Child": {
                    "type": "object",
                    "properties": {"value": {"type": "integer"}},
                },
            }
        }
    }

    graph = build_schema_graph(spec)
    assert graph["Parent"] == ["Child"]
    order = topo_order(graph)
    assert order.index("Child") < order.index("Parent")

    registry = SchemaRegistry(spec)
    assert registry.ordered_children("Parent") == ["Child"]


def test_topo_order_cycle_detection():
    graph = {"A": ["B"], "B": ["A"]}
    order = topo_order(graph)
    assert set(order) == {"A", "B"}


def test_resolve_schema_with_cycle():
    spec = {
        "components": {
            "schemas": {
                "Alpha": {
                    "type": "object",
                    "required": ["id", "beta"],
                    "properties": {
                        "id": {"type": "string", "minLength": 3},
                        "beta": {"$ref": "#/components/schemas/Beta"},
                    },
                },
                "Beta": {
                    "type": "object",
                    "required": ["name", "alpha"],
                    "properties": {
                        "name": {"type": "string"},
                        "alpha": {
                            "anyOf": [
                                {"type": "string", "minLength": 2},
                                {"$ref": "#/components/schemas/Alpha"},
                            ]
                        },
                    },
                },
            }
        }
    }
    registry = SchemaRegistry(spec)
    payload = registry.resolve_schema("Alpha", seed=42)
    assert payload["id"]
    assert "beta" in payload
    beta = payload["beta"]
    assert beta["name"]
    assert isinstance(beta["alpha"], str)
