"""Graph-based data generator using GPT API.

Generates sample data by:
1. Building component dependency graph
2. Identifying leaves (components with no dependencies)
3. Generating data from leaves up (topological order)
4. Creating references to previously generated records
5. Using GPT to fill in realistic field values
"""

from __future__ import annotations

from collections import deque
from typing import Any, Dict, List, Optional, Set

from ingestion import (
    construct_component_graph,
    get_component_entry,
    get_component_properties,
)

from database import GeneratedRecord, db_session
from sqlmodel import select

# Try to import openai, but make it optional
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    openai = None


class GraphDataGenerator:
    """Generate realistic sample data using component dependency graph."""
    
    def __init__(self, api_slug: str, openai_api_key: Optional[str] = None):
        self.api_slug = api_slug
        self.openai_client = None
        
        # Use environment variable or provided key
        import os
        api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        
        if api_key and OPENAI_AVAILABLE:
            try:
                # Try new OpenAI SDK format
                import openai
                if hasattr(openai, 'OpenAI'):
                    self.openai_client = openai.OpenAI(api_key=api_key)
                else:
                    # Fallback to old format
                    openai.api_key = api_key
                    self.openai_client = openai
            except Exception:
                self.openai_client = None
        
        # Track generated records to create references
        self._generated_records: Dict[str, List[Dict[str, Any]]] = {}
        # Track component order (topological sort)
        self._component_order: List[str] = []
    
    def generate_all(
        self,
        count_per_component: Optional[Dict[str, int]] = None,
        seed_account_id: Optional[str] = None,
        store_in_db: bool = True,
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Generate sample data for all components, starting from leaves.
        
        Args:
            count_per_component: Number of records to generate per component
            seed_account_id: Account ID to associate generated data with (for account-scoped storage)
            store_in_db: If True, store records in GeneratedRecord database table
        
        Returns:
            Dict mapping component_name -> list of records
        """
        # Build dependency graph
        graph = construct_component_graph(self.api_slug)
        
        # Get topological order (leaves first)
        component_order = self._topological_sort(graph)
        self._component_order = component_order
        
        count_per_component = count_per_component or {}
        result: Dict[str, List[Dict[str, Any]]] = {}
        
        # Generate data in topological order
        for component_name in component_order:
            count = count_per_component.get(component_name, 3)
            records = self._generate_component_records(
                component_name,
                count,
                graph,
                seed_account_id=seed_account_id,
                store_in_db=store_in_db,
            )
            result[component_name] = records
            self._generated_records[component_name] = records
        
        return result
    
    def _topological_sort(self, graph: Dict[str, Any]) -> List[str]:
        """
        Return components in topological order (leaves first).
        
        Leaves are components with no dependencies (dependent_count = 0).
        """
        nodes = {node["component_name"]: node for node in graph["nodes"]}
        edges = graph["edges"]
        
        # Build adjacency list and indegree count
        adjacency: Dict[str, List[str]] = {name: [] for name in nodes.keys()}
        indegree: Dict[str, int] = {name: 0 for name in nodes.keys()}
        
        for edge in edges:
            source = edge["source"]
            target = edge["target"]
            # Source depends on target (source -> target means source references target)
            adjacency[target].append(source)
            indegree[source] += 1
        
        # Start with leaves (indegree = 0)
        queue = deque([name for name, degree in indegree.items() if degree == 0])
        result: List[str] = []
        
        while queue:
            current = queue.popleft()
            result.append(current)
            
            # Process dependents
            for dependent in adjacency[current]:
                indegree[dependent] -= 1
                if indegree[dependent] == 0:
                    queue.append(dependent)
        
        # Handle any remaining components (cycles or isolated)
        remaining = [name for name in nodes.keys() if name not in result]
        result.extend(remaining)
        
        return result
    
    def _generate_component_records(
        self,
        component_name: str,
        count: int,
        graph: Dict[str, Any],
        seed_account_id: Optional[str] = None,
        store_in_db: bool = True,
    ) -> List[Dict[str, Any]]:
        """Generate records for a single component."""
        entry = get_component_entry(self.api_slug, component_name)
        if not entry:
            return []
        
        properties = get_component_properties(entry)
        schema = entry.get("schema", {})
        
        records = []
        for idx in range(count):
            record = self._build_record(
                component_name,
                properties,
                schema,
                idx,
                graph,
            )
            
            # Store in database by default (or account-scoped if account provided)
            if store_in_db:
                if seed_account_id:
                    # For account-scoped storage (standalone APIs)
                    # This would need account-scoped DB storage logic
                    pass
                else:
                    # Store in GeneratedRecord table
                    self._store_record(component_name, record, account_id=None)
            
            records.append(record)
        
        return records
    
    def _build_record(
        self,
        component_name: str,
        properties: List[Dict[str, Any]],
        schema: Dict[str, Any],
        index: int,
        graph: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Build a single record with realistic values."""
        record: Dict[str, Any] = {
            "_generated": True,
            "_component": component_name,
            "_index": index,
        }
        
        # Get component dependencies
        nodes = {node["component_name"]: node for node in graph["nodes"]}
        component_node = nodes.get(component_name, {})
        references = component_node.get("references", [])
        
        for prop in properties:
            prop_name = prop["property_name"]
            prop_type = prop.get("property_type")
            prop_ref = prop.get("reference")
            
            # Handle references to other components
            if prop_ref:
                referenced_component = self._resolve_ref(prop_ref)
                if referenced_component and referenced_component in self._generated_records:
                    # Reference an existing record
                    existing = self._generated_records[referenced_component]
                    if existing:
                        # Use a record from previously generated ones
                        ref_idx = index % len(existing)
                        ref_record = existing[ref_idx]
                        record[prop_name] = ref_record.get("id")
                    continue
            
            # Generate realistic value using GPT or heuristics
            record[prop_name] = self._generate_field_value(
                component_name,
                prop_name,
                prop_type,
                index,
            )
        
        # Ensure ID exists
        if "id" not in record:
            record["id"] = f"{component_name.lower()}_{index}"
        
        return record
    
    def _resolve_ref(self, ref: str) -> Optional[str]:
        """Resolve a $ref to component name."""
        if not isinstance(ref, str):
            return None
        if ref.startswith("#/components/schemas/"):
            return ref.split("/")[-1]
        return None
    
    def _generate_field_value(
        self,
        component_name: str,
        field_name: str,
        field_type: Optional[str],
        index: int,
    ) -> Any:
        """
        Generate a realistic value for a field.
        
        Uses GPT API if available, otherwise falls back to heuristics.
        """
        field_lower = field_name.lower()
        
        # Try GPT generation first
        if self.openai_client:
            try:
                return self._generate_with_gpt(component_name, field_name, field_type, index)
            except Exception:
                # Fall back to heuristics if GPT fails
                pass
        
        # Fallback to heuristics
        return self._generate_heuristic(field_name, field_type, index)
    
    def _generate_with_gpt(
        self,
        component_name: str,
        field_name: str,
        field_type: Optional[str],
        index: int,
    ) -> str:
        """Use GPT to generate realistic field value."""
        prompt = f"""Generate a realistic sample value for:
- Component: {component_name}
- Field: {field_name}
- Type: {field_type or "string"}
- Example index: {index}

Return ONLY the value, nothing else. For example:
- username -> "john_doe"
- email -> "user@example.com"
- amount -> 100
- status -> "active"
- created_at -> "2024-01-15T10:30:00Z"

Value:"""
        
        try:
            # Try new OpenAI SDK format first
            if hasattr(self.openai_client, 'chat') and hasattr(self.openai_client.chat, 'completions'):
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a data generator. Return only the requested value."},
                        {"role": "user", "content": prompt},
                    ],
                    max_tokens=50,
                    temperature=0.7,
                )
                value = response.choices[0].message.content.strip()
            else:
                # Fallback to old format
                response = self.openai_client.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a data generator. Return only the requested value."},
                        {"role": "user", "content": prompt},
                    ],
                    max_tokens=50,
                    temperature=0.7,
                )
                value = response.choices[0].message.content.strip()
            
            # Try to parse based on type
            if field_type == "integer" or "int" in str(field_type):
                try:
                    return int(value)
                except ValueError:
                    pass
            elif field_type == "number" or "float" in str(field_type):
                try:
                    return float(value)
                except ValueError:
                    pass
            elif field_type == "boolean" or "bool" in str(field_type):
                return value.lower() in ("true", "1", "yes")
            
            return value
        except Exception:
            # Fall back to heuristics
            return self._generate_heuristic(field_name, field_type, index)
    
    def _generate_heuristic(
        self,
        field_name: str,
        field_type: Optional[str],
        index: int,
    ) -> Any:
        """Generate value using heuristics when GPT is unavailable."""
        field_lower = field_name.lower()
        
        # ID fields
        if field_lower in ("id", "uuid") or field_lower.endswith("_id"):
            base = field_lower.replace("_id", "").replace("id", "")
            return f"{base}_{index}" if base else f"id_{index}"
        
        # Name fields
        if "name" in field_lower:
            if "user" in field_lower:
                return f"user_{index}"
            elif "account" in field_lower:
                return f"Account {index}"
            else:
                return f"{field_name} {index}"
        
        # Email
        if "email" in field_lower:
            return f"user{index}@example.com"
        
        # Status
        if "status" in field_lower:
            return "active" if index % 2 == 0 else "pending"
        
        # Dates
        if "created" in field_lower or "updated" in field_lower or "date" in field_lower:
            from datetime import datetime, timezone
            return datetime.now(timezone.utc).isoformat()
        
        # Amount/money
        if "amount" in field_lower or "price" in field_lower or "cost" in field_lower:
            return (index + 1) * 100
        
        # Boolean
        if field_type == "boolean" or "bool" in str(field_type):
            return index % 2 == 0
        
        # Numbers
        if field_type in ("integer", "number"):
            return index * 10
        
        # Default
        return f"{field_lower}_{index}"
    
    def _store_record(
        self,
        component_name: str,
        record: Dict[str, Any],
        account_id: Optional[str] = None,
    ) -> None:
        """Store generated record in GeneratedRecord database table."""
        with db_session() as session:
            record_id = str(record.get("id", record.get("_index", 0)))
            
            # Check if exists
            existing = session.exec(
                select(GeneratedRecord)
                .where(GeneratedRecord.api_slug == self.api_slug)
                .where(GeneratedRecord.component_name == component_name)
                .where(GeneratedRecord.record_key == record_id)
            ).first()
            
            if existing:
                existing.payload = record
            else:
                session.add(
                    GeneratedRecord(
                        api_slug=self.api_slug,
                        component_name=component_name,
                        record_key=record_id,
                        payload=record,
                    )
                )


def generate_graph_based_data(
    api_slug: str,
    count_per_component: Optional[Dict[str, int]] = None,
    openai_api_key: Optional[str] = None,
    seed_account_id: Optional[str] = None,
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Generate sample data for all components using dependency graph.
    
    Example:
        data = generate_graph_based_data(
            api_slug="stripe",
            count_per_component={"account": 5, "customer": 10},
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            seed_account_id="acct_123"
        )
    """
    generator = GraphDataGenerator(api_slug, openai_api_key)
    return generator.generate_all(count_per_component, seed_account_id)

