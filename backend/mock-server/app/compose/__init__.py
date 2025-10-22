from __future__ import annotations

import copy
from typing import Any, Dict

try:
    from ..util.refs import REF_RE
except ImportError:  # pragma: no cover
    from util.refs import REF_RE  # type: ignore


def compose_schema(
    schema_name: str,
    schema: Dict[str, Any],
    children: Dict[str, Any],
    context,
) -> Any:
    """Compose a non-leaf schema from its child payloads."""
    return _compose_value(schema_name, schema, children, context, path=schema_name)


def _compose_value(
    schema_name: str,
    schema: Dict[str, Any],
    children: Dict[str, Any],
    context,
    path: str,
) -> Any:
    if "$ref" in schema:
        match = REF_RE.match(schema["$ref"])
        if match:
            name = match.group("name")
            payload = children.get(name)
            if payload is not None:
                return copy.deepcopy(payload)
            return context.resolve(name)
        raise ValueError(f"Unsupported external $ref {schema['$ref']}")

    if "const" in schema:
        return copy.deepcopy(schema["const"])

    if "enum" in schema:
        return copy.deepcopy(schema["enum"][0])

    if "allOf" in schema:
        result: Dict[str, Any] = {}
        for idx, subschema in enumerate(schema["allOf"]):
            fragment = _compose_value(
                f"{schema_name}.allOf{idx}", subschema, children, context, path
            )
            if isinstance(fragment, dict):
                result.update(fragment)
        return result

    if "oneOf" in schema:
        choice = context.faker.random_element(schema["oneOf"])
        return _compose_value(schema_name, choice, children, context, path)

    if "anyOf" in schema:
        choice = context.faker.random_element(schema["anyOf"])
        return _compose_value(schema_name, choice, children, context, path)

    schema_type = schema.get("type")
    if isinstance(schema_type, list):
        non_null = [t for t in schema_type if t != "null"]
        schema_type = non_null[0] if non_null else schema_type[0]

    if schema_type == "object" or (
        not schema_type and ("properties" in schema or "additionalProperties" in schema)
    ):
        return _compose_object(schema_name, schema, children, context, path)

    if schema_type == "array":
        return _compose_array(schema_name, schema, children, context, path)

    # Primitive fallback uses the leaf factory utilities.
    try:
        from ..factories import _generate_string, _generate_integer, _generate_number  # type: ignore  # noqa: E402
    except ImportError:  # pragma: no cover
        from factories import _generate_string, _generate_integer, _generate_number  # type: ignore  # noqa: E402

    if schema_type == "string" or schema_type is None:
        return _generate_string(schema, context.faker, path)
    if schema_type == "integer":
        return _generate_integer(schema, context.faker)
    if schema_type == "number":
        return _generate_number(schema, context.faker)
    if schema_type == "boolean":
        return context.faker.pybool()
    if schema_type == "null":
        return None
    return {}


def _compose_object(
    schema_name: str,
    schema: Dict[str, Any],
    children: Dict[str, Any],
    context,
    path: str,
) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    properties = schema.get("properties") or {}
    required = set(schema.get("required") or [])

    for prop_name, prop_schema in properties.items():
        if "$ref" in prop_schema:
            match = REF_RE.match(prop_schema["$ref"])
            if match:
                child_name = match.group("name")
                payload = children.get(child_name)
                if payload is None:
                    payload = context.resolve(child_name)
                result[prop_name] = copy.deepcopy(payload)
            continue
        if prop_name in required or context.faker.pybool():
            result[prop_name] = _compose_value(
                f"{schema_name}.{prop_name}",
                prop_schema,
                children,
                context,
                f"{path}.{prop_name}",
            )

    additional = schema.get("additionalProperties")
    if isinstance(additional, dict):
        key = context.faker.pystr(min_chars=5, max_chars=12)
        if "$ref" in additional:
            match = REF_RE.match(additional["$ref"])
            if match:
                child_name = match.group("name")
                payload = children.get(child_name)
                if payload is None:
                    payload = context.resolve(child_name)
                result[key] = copy.deepcopy(payload)
        else:
            result[key] = _compose_value(
                f"{schema_name}.additional",
                additional,
                children,
                context,
                f"{path}.additional",
            )
    return result


def _compose_array(
    schema_name: str,
    schema: Dict[str, Any],
    children: Dict[str, Any],
    context,
    path: str,
) -> Any:
    items_schema = schema.get("items") or {}
    min_items = schema.get("minItems", 1)
    max_items = schema.get("maxItems", max(min_items, 3))
    if max_items < min_items:
        max_items = min_items
    count = min_items
    if max_items > min_items:
        count = context.faker.random_int(min_items, max_items)
    results = []
    for idx in range(count):
        if "$ref" in items_schema:
            match = REF_RE.match(items_schema["$ref"])
            if match:
                child_name = match.group("name")
                payload = children.get(child_name)
                if payload is None:
                    payload = context.resolve(child_name)
                results.append(copy.deepcopy(payload))
                continue
        results.append(
            _compose_value(
                f"{schema_name}[{idx}]",
                items_schema,
                children,
                context,
                f"{path}[{idx}]",
            )
        )
    return results
