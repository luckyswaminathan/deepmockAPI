from __future__ import annotations

from typing import Any, Dict

from fastapi import HTTPException
from jsonschema import Draft7Validator, ValidationError
from jsonschema import RefResolver


class SpecValidator:
    """Validate payloads against schemas defined in the OpenAPI document."""

    def __init__(self, spec: Dict[str, Any]):
        self.spec = spec
        self.resolver = RefResolver.from_schema(spec)
        self._validators: Dict[str, Draft7Validator] = {}

    def validate(self, schema_name: str, payload: Any) -> None:
        validator = self._validators.get(schema_name)
        if validator is None:
            schema_ref = {"$ref": f"#/components/schemas/{schema_name}"}
            validator = Draft7Validator(schema_ref, resolver=self.resolver)
            self._validators[schema_name] = validator
        try:
            validator.validate(payload)
        except ValidationError as exc:  # pragma: no cover - surface via HTTP
            raise HTTPException(
                status_code=500,
                detail={
                    "message": "Synthesised payload failed schema validation",
                    "schema": schema_name,
                    "error": exc.message,
                    "path": list(exc.path),
                },
            ) from exc
