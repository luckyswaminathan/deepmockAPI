from jsonschema import validate

from app.factories import generate_leaf
from app.registry import SchemaRegistry


def test_generate_leaf_object_required_fields():
    spec = {
        "components": {
            "schemas": {
                "Simple": {
                    "type": "object",
                    "required": ["name"],
                    "properties": {
                        "name": {"type": "string", "minLength": 3},
                        "age": {"type": "integer", "minimum": 18, "maximum": 30},
                    },
                }
            }
        }
    }
    registry = SchemaRegistry(spec)
    schema = registry.get_schema("Simple")
    context = registry._create_context(seed=1234)
    payload = generate_leaf("Simple", schema, context)
    validate(instance=payload, schema=schema)
    assert "name" in payload
    assert len(payload["name"]) >= 3


def test_generate_leaf_array_min_items():
    spec = {
        "components": {
            "schemas": {
                "Arr": {
                    "type": "array",
                    "minItems": 2,
                    "items": {"type": "integer", "minimum": 1, "maximum": 5},
                }
            }
        }
    }
    registry = SchemaRegistry(spec)
    schema = registry.get_schema("Arr")
    context = registry._create_context(seed=99)
    payload = generate_leaf("Arr", schema, context)
    validate(instance=payload, schema=schema)
    assert len(payload) >= 2
