"""Utility functions for RL module."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel


def model_to_json(model: BaseModel) -> str:
    """
    Convert Pydantic model to JSON string.
    Compatible with both Pydantic v1 and v2.
    """
    # Try Pydantic v2 method first
    if hasattr(model, "model_dump_json"):
        return model.model_dump_json()
    # Fallback to Pydantic v1 method
    elif hasattr(model, "json"):
        return model.json()
    else:
        # Last resort: use dict and json.dumps
        import json
        if hasattr(model, "model_dump"):
            return json.dumps(model.model_dump())
        elif hasattr(model, "dict"):
            return json.dumps(model.dict())
        else:
            raise AttributeError(f"Model {type(model)} has no JSON serialization method")


def json_to_model(model_class: type[BaseModel], json_str: str) -> BaseModel:
    """
    Parse JSON string to Pydantic model.
    Compatible with both Pydantic v1 and v2.
    """
    # Try Pydantic v2 method first
    if hasattr(model_class, "model_validate_json"):
        return model_class.model_validate_json(json_str)
    # Fallback to Pydantic v1 method
    elif hasattr(model_class, "parse_raw"):
        return model_class.parse_raw(json_str)
    else:
        # Last resort: parse JSON and use constructor
        import json
        data = json.loads(json_str)
        if hasattr(model_class, "model_validate"):
            return model_class.model_validate(data)
        else:
            return model_class(**data)

