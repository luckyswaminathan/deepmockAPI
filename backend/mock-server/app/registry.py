from __future__ import annotations

import re
import copy
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set

from faker import Faker

try:
    from .compose import compose_schema
    from .factories import generate_leaf
    from .util.refs import REF_RE
except ImportError:  # pragma: no cover
    from compose import compose_schema  # type: ignore
    from factories import generate_leaf  # type: ignore
    from util.refs import REF_RE  # type: ignore

try:
    import yaml
except ImportError as exc:  # pragma: no cover - handled via requirements
    raise RuntimeError("PyYAML is required to load OpenAPI specifications.") from exc

# REF_RE imported from util.refs to avoid circular imports


def load_spec(path: Path | str = "openapi.yaml") -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _iter_refs(node: Any) -> Iterable[str]:
    if isinstance(node, dict):
        if "$ref" in node:
            match = REF_RE.match(node["$ref"])
            if match:
                yield match.group("name")
        for value in node.values():
            yield from _iter_refs(value)
    elif isinstance(node, list):
        for item in node:
            yield from _iter_refs(item)


def build_schema_graph(spec: Dict[str, Any]) -> Dict[str, List[str]]:
    components = spec.get("components", {}).get("schemas", {}) or {}
    graph: Dict[str, List[str]] = {name: [] for name in components.keys()}
    for parent, schema in components.items():
        children = set(_iter_refs(schema))
        for child in children:
            if child in graph:
                graph[parent].append(child)
    return graph


def topo_order(graph: Dict[str, List[str]]) -> List[str]:
    indegree: Dict[str, int] = {node: 0 for node in graph}
    for source, targets in graph.items():
        for target in targets:
            indegree[target] = indegree.get(target, 0) + 1
    queue = deque([node for node, deg in indegree.items() if deg == 0])
    order: List[str] = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for target in graph.get(node, []):
            indegree[target] -= 1
            if indegree[target] == 0:
                queue.append(target)
    if len(order) != len(graph):
        remaining = [node for node in graph if node not in order]
        order.extend(sorted(remaining))
    return order


@dataclass
class ResolutionContext:
    registry: "SchemaRegistry"
    params: Dict[str, Any]
    faker: Faker
    memo: Dict[str, Any]
    stack: List[str] = field(default_factory=list)

    def resolve(self, schema_name: str) -> Any:
        if schema_name in self.memo:
            return copy.deepcopy(self.memo[schema_name])
        if schema_name in self.stack:
            return self.registry.generate_stub(schema_name)
        schema = self.registry.get_schema(schema_name)
        ordered_children = self.registry.ordered_children(schema_name)
        self.stack.append(schema_name)
        try:
            if not ordered_children:
                result = generate_leaf(schema_name, schema, self)
            else:
                child_payloads = {name: self.resolve(name) for name in ordered_children}
                result = compose_schema(schema_name, schema, child_payloads, self)
        finally:
            self.stack.pop()
        self.memo[schema_name] = copy.deepcopy(result)
        return copy.deepcopy(result)


class SchemaRegistry:
    """Registry responsible for schema storage and materialisation."""

    def __init__(self, spec: Dict[str, Any]):
        self.spec = spec
        self.schemas: Dict[str, Any] = (
            spec.get("components", {}).get("schemas", {}) or {}
        )
        self.graph = build_schema_graph(spec)
        self.order = topo_order(self.graph)
        self._order_index = {name: idx for idx, name in enumerate(self.order)}
        self._stub_cache: Dict[str, Any] = {}

    def get_schema(self, name: str) -> Dict[str, Any]:
        if name not in self.schemas:
            raise KeyError(f"Schema '{name}' not found in components.")
        return self.schemas[name]

    def resolve_schema(
        self,
        name: str,
        params: Optional[Dict[str, Any]] = None,
        seed: Optional[int] = None,
    ) -> Any:
        ctx = self._create_context(params=params, seed=seed)
        return ctx.resolve(name)

    def _create_context(
        self,
        params: Optional[Dict[str, Any]] = None,
        seed: Optional[int] = None,
    ) -> ResolutionContext:
        faker = Faker()
        if seed is not None:
            faker.seed_instance(seed)
        return ResolutionContext(
            registry=self,
            params=params or {},
            faker=faker,
            memo={},
        )

    def child_schemas(self, name: str) -> List[str]:
        return list(self.graph.get(name, []))

    def ordered_children(self, name: str) -> List[str]:
        children = self.graph.get(name, [])
        return sorted(children, key=lambda item: self._order_index.get(item, 0))

    def is_leaf(self, name: str) -> bool:
        return not self.graph.get(name)

    def generate_stub(self, name: str) -> Any:
        cached = self._stub_cache.get(name)
        if cached is not None:
            return copy.deepcopy(cached)
        stub = self._build_stub(name, path=tuple())
        self._stub_cache[name] = stub
        return copy.deepcopy(stub)

    def _build_stub(self, name: str, path: tuple[str, ...]) -> Any:
        if name in path:
            return {}
        schema = self.get_schema(name)
        minimal = self._minimal_schema(schema)
        refs = self._required_refs(minimal)
        next_path = path + (name,)
        if not refs:
            context = _StubContext(self, next_path)
            return generate_leaf(name, minimal, context)
        child_payloads: Dict[str, Any] = {}
        for child in refs:
            child_payloads[child] = self._build_stub(child, next_path)
        context = _StubContext(self, next_path)
        return compose_schema(name, minimal, child_payloads, context)

    def _minimal_schema(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        if "$ref" in schema:
            return {"$ref": schema["$ref"]}
        if "const" in schema:
            return {"const": schema["const"]}
        if "enum" in schema:
            return {"enum": list(schema["enum"])}
        if "allOf" in schema:
            return {"allOf": [self._minimal_schema(item) for item in schema["allOf"]]}
        if "oneOf" in schema:
            option = self._select_option(schema["oneOf"])
            return self._minimal_schema(option)
        if "anyOf" in schema:
            option = self._select_option(schema["anyOf"])
            return self._minimal_schema(option)

        schema_type = schema.get("type")
        if isinstance(schema_type, list):
            non_null = [t for t in schema_type if t != "null"]
            schema_type = non_null[0] if non_null else schema_type[0]

        minimal = copy.deepcopy(schema)

        if schema_type == "object" or (
            not schema_type and ("properties" in schema or "additionalProperties" in schema)
        ):
            properties = schema.get("properties") or {}
            required = [prop for prop in schema.get("required", []) if prop in properties]
            minimal["properties"] = {
                prop: self._minimal_schema(properties[prop]) for prop in required
            }
            minimal["required"] = required
            minimal["additionalProperties"] = False
            for key in list(minimal.keys()):
                if key.startswith("x-"):
                    minimal.pop(key, None)
            return minimal

        if schema_type == "array":
            items = schema.get("items") or {}
            minimal["items"] = self._minimal_schema(items)
            min_items = schema.get("minItems", 0)
            minimal["minItems"] = min_items
            if min_items == 0:
                minimal["maxItems"] = 0
            else:
                minimal["maxItems"] = min_items
            return minimal

        return minimal

    def _select_option(self, options: List[Dict[str, Any]]) -> Dict[str, Any]:
        def weight(option: Dict[str, Any]) -> int:
            return sum(1 for _ in _iter_refs(option))

        return min(options, key=weight)

    def _required_refs(self, schema: Dict[str, Any]) -> List[str]:
        refs: Set[str] = set()

        def walk(node: Any) -> None:
            if isinstance(node, dict):
                ref = node.get("$ref")
                if ref:
                    match = REF_RE.match(ref)
                    if match:
                        refs.add(match.group("name"))
                    return
                if "allOf" in node:
                    for item in node["allOf"]:
                        walk(item)
                    return
                if "oneOf" in node:
                    option = self._select_option(node["oneOf"])
                    walk(option)
                    return
                if "anyOf" in node:
                    option = self._select_option(node["anyOf"])
                    walk(option)
                    return
                schema_type = node.get("type")
                if isinstance(schema_type, list):
                    non_null = [t for t in schema_type if t != "null"]
                    schema_type = non_null[0] if non_null else schema_type[0]
                if schema_type == "object" or (
                    not schema_type and ("properties" in node or "additionalProperties" in node)
                ):
                    props = node.get("properties") or {}
                    required = node.get("required") or []
                    for prop in required:
                        if prop in props:
                            walk(props[prop])
                    return
                if schema_type == "array":
                    min_items = node.get("minItems", 0)
                    if min_items == 0:
                        return
                    walk(node.get("items") or {})
                    return
            elif isinstance(node, list):
                for item in node:
                    walk(item)

        walk(schema)
        return sorted(refs)


class _StubContext:
    def __init__(self, registry: "SchemaRegistry", path: tuple[str, ...]):
        self.registry = registry
        self.path = path
        self.faker = Faker()

    def resolve(self, schema_name: str) -> Any:
        if schema_name in self.path:
            return {}
        return self.registry._build_stub(schema_name, self.path)
