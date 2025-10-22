from __future__ import annotations

import copy
from typing import Any, Dict, List

from faker import Faker

try:
    from ..util.refs import REF_RE
except ImportError:  # pragma: no cover
    from util.refs import REF_RE  # type: ignore


def generate_leaf(schema_name: str, schema: Dict[str, Any], context) -> Any:
    """Generate data for a leaf schema using Faker-driven synthesis."""
    return _generate_value(schema_name, schema, context, path=schema_name)


def _generate_value(
    schema_name: str,
    schema: Dict[str, Any],
    context,
    path: str,
) -> Any:
    if "$ref" in schema:
        # Leaf schemas should not contain refs; route via registry if encountered.
        ref = schema["$ref"]
        match = REF_RE.match(ref)
        if match:
            return context.resolve(match.group("name"))
        raise ValueError(f"Unsupported external $ref {ref} in leaf schema '{schema_name}'")

    if "const" in schema:
        return copy.deepcopy(schema["const"])

    if "enum" in schema:
        return copy.deepcopy(schema["enum"][0])

    if "default" in schema:
        return copy.deepcopy(schema["default"])

    if "allOf" in schema:
        return _generate_all_of(schema_name, schema["allOf"], context, path)

    if "oneOf" in schema:
        choice = context.faker.random_element(schema["oneOf"])
        return _generate_value(schema_name, choice, context, f"{path}_oneOf")

    if "anyOf" in schema:
        choice = context.faker.random_element(schema["anyOf"])
        return _generate_value(schema_name, choice, context, f"{path}_anyOf")

    schema_type = schema.get("type")
    if isinstance(schema_type, list):
        non_null = [t for t in schema_type if t != "null"]
        schema_type = non_null[0] if non_null else schema_type[0]

    if schema_type == "object" or (
        not schema_type and ("properties" in schema or "additionalProperties" in schema)
    ):
        return _generate_object(schema_name, schema, context, path)
    if schema_type == "array":
        return _generate_array(schema_name, schema, context, path)
    if schema_type == "integer":
        return _generate_integer(schema, context.faker)
    if schema_type == "number":
        return _generate_number(schema, context.faker)
    if schema_type == "boolean":
        return context.faker.pybool()
    if schema_type == "string" or schema_type is None:
        return _generate_string(schema, context.faker, path)
    if schema_type == "null":
        return None

    # Fallback for unexpected shapes.
    return {}


def _generate_object(
    schema_name: str, schema: Dict[str, Any], context, path: str
) -> Dict[str, Any]:
    faker: Faker = context.faker
    result: Dict[str, Any] = {}
    required = set(schema.get("required") or [])
    properties = schema.get("properties") or {}

    for prop_name, prop_schema in properties.items():
        if "$ref" in prop_schema:
            match = REF_RE.match(prop_schema["$ref"])
            if match:
                result[prop_name] = context.resolve(match.group("name"))
            continue
        if prop_name in required or faker.pybool():
            result[prop_name] = _generate_value(
                f"{schema_name}.{prop_name}", prop_schema, context, f"{path}.{prop_name}"
            )

    additional = schema.get("additionalProperties")
    if isinstance(additional, dict):
        key = faker.pystr(min_chars=5, max_chars=12)
        if "$ref" in additional:
            match = REF_RE.match(additional["$ref"])
            if match:
                result[key] = context.resolve(match.group("name"))
        else:
            result[key] = _generate_value(
                f"{schema_name}.additional", additional, context, f"{path}.additional"
            )

    return result


def _generate_array(
    schema_name: str, schema: Dict[str, Any], context, path: str
) -> List[Any]:
    faker: Faker = context.faker
    min_items = schema.get("minItems", 1)
    max_items = schema.get("maxItems", max(min_items, 3))
    if max_items < min_items:
        max_items = min_items
    count = min_items
    if max_items > min_items:
        count = faker.random_int(min_items, max_items)
    items_schema = schema.get("items") or {}
    result = []
    for idx in range(count):
        if "$ref" in items_schema:
            match = REF_RE.match(items_schema["$ref"])
            if match:
                result.append(context.resolve(match.group("name")))
            continue
        result.append(
            _generate_value(
                f"{schema_name}[{idx}]",
                items_schema,
                context,
                f"{path}[{idx}]",
            )
        )
    return result


def _generate_integer(schema: Dict[str, Any], faker: Faker) -> int:
    minimum = schema.get("minimum", 0)
    maximum = schema.get("maximum", minimum + 100)
    exclusive_min = schema.get("exclusiveMinimum")
    exclusive_max = schema.get("exclusiveMaximum")
    if exclusive_min is not None:
        minimum = exclusive_min + 1
    if exclusive_max is not None:
        maximum = exclusive_max - 1
    if maximum < minimum:
        maximum = minimum
    return faker.random_int(minimum, maximum)


def _generate_number(schema: Dict[str, Any], faker: Faker) -> float:
    minimum = schema.get("minimum", 0.0)
    maximum = schema.get("maximum", minimum + 100.0)
    if maximum < minimum:
        maximum = minimum + 100.0
    return float(faker.pyfloat(minimum=minimum, maximum=maximum, right_digits=2))


def _generate_string(schema: Dict[str, Any], faker: Faker, path: str) -> str:
    fmt = schema.get("format")
    pattern = schema.get("pattern")
    min_length = schema.get("minLength", 1)
    max_length = schema.get("maxLength", max(min_length, 12))

    if schema.get("format") == "email":
        return faker.email()
    if fmt in {"uuid", "uuid4"}:
        return faker.uuid4()
    if fmt in {"date", "date-time"}:
        return faker.iso8601()
    if fmt == "uri":
        return faker.url()
    if fmt == "phone":
        return faker.phone_number()
    if fmt == "currency":
        return faker.currency_code()
    if pattern:
        # Produce a simple placeholder honoring length bounds; not full regex support.
        size = min(max_length, max(min_length, 8))
        return faker.pystr(min_chars=size, max_chars=size)

    if max_length <= min_length:
        size = max_length
    else:
        size = faker.random_int(min_length, max_length)
    return faker.pystr(min_chars=size, max_chars=max(size, min_length))


def _generate_all_of(
    schema_name: str, subschemas, context, path: str
) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    for idx, subschema in enumerate(subschemas):
        value = _generate_value(
            f"{schema_name}.allOf{idx}", subschema, context, f"{path}.allOf_{idx}"
        )
        if isinstance(value, dict):
            result.update(value)
    return result
