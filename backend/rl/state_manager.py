"""State Manager for RL state tracking."""

from __future__ import annotations

import hashlib
import json
import sys
from typing import Any, Dict, List, Optional

from .models import State
from .redis_client import get_redis_client
from .utils import model_to_json, json_to_model

# Import runtime functions for database access
try:
    from reverse import runtime
except ImportError:
    # Fallback for standalone usage
    try:
        import runtime as runtime_module
        runtime = runtime_module
    except ImportError:
        runtime = None

# Import database models and functions
try:
    from database import GeneratedRecord, RLStateRecord, db_session
    from sqlmodel import delete, select
except ImportError:
    GeneratedRecord = None
    RLStateRecord = None
    db_session = None
    delete = None
    select = None


class StateManager:
    """Manages RL states: creation, storage, retrieval, and restoration."""
    
    def __init__(self):
        self.redis = get_redis_client()
    
    def _state_key(self, state_id: str) -> str:
        """Get Redis key for a state."""
        return f"state:{state_id}"
    
    def _state_children_key(self, state_id: str) -> str:
        """Get Redis key for state children set."""
        return f"state:{state_id}:children"
    
    def _state_actions_key(self, state_id: str) -> str:
        """Get Redis key for state actions set."""
        return f"state:{state_id}:actions"
    
    def _api_states_key(self, api_slug: str) -> str:
        """Get Redis key for API states index."""
        return f"api:{api_slug}:states"
    
    def _generate_state_id(self, modified_components: Dict[str, List[Dict[str, Any]]]) -> str:
        """Generate deterministic state ID from modified_components."""
        # Sort components and records for deterministic hashing
        sorted_data = {}
        for component_name in sorted(modified_components.keys()):
            records = modified_components[component_name]
            # Sort records by their ID or first key
            sorted_records = sorted(
                records,
                key=lambda r: str(r.get("id", r.get("record_key", "")))
            )
            sorted_data[component_name] = sorted_records
        
        # Serialize and hash
        serialized = json.dumps(sorted_data, sort_keys=True, default=str)
        state_hash = hashlib.sha256(serialized.encode()).hexdigest()[:16]
        return f"state_{state_hash}"
    
    def create_state(
        self,
        api_slug: str,
        parent_state_id: Optional[str] = None,
        action_id: Optional[str] = None,
        modified_components: Optional[Dict[str, List[Dict[str, Any]]]] = None,
    ) -> str:
        """
        Create a new state from parent state + modified components.
        
        Args:
            api_slug: API identifier
            parent_state_id: Parent state ID (None for initial state)
            action_id: Action that led to this state
            modified_components: Newly modified components. If None, detects from DB.
        
        Returns:
            state_id
        """
        # Get parent state's modified_components
        parent_modified = {}
        action_path = []
        
        if parent_state_id:
            parent_state = self.get_state(parent_state_id, reconstruct_if_missing=True)
            parent_modified = parent_state.modified_components.copy()
            action_path = parent_state.action_path.copy()
            if action_id:
                action_path.append(action_id)
        elif action_id:
            action_path = [action_id]
        
        # Merge with new modifications
        if modified_components is None:
            # Detect from database
            modified_components = self.detect_modified_components(api_slug, parent_state_id)
        
        # Merge parent + new modifications
        merged_components = parent_modified.copy()
        for component_name, records in modified_components.items():
            # For each component, merge records (update existing, add new)
            if component_name not in merged_components:
                merged_components[component_name] = []
            
            # Create a map of existing records by ID
            existing_map = {
                str(r.get("id", r.get("record_key", ""))): r
                for r in merged_components[component_name]
            }
            
            # Update/add records
            for record in records:
                record_id = str(record.get("id", record.get("record_key", "")))
                existing_map[record_id] = record
            
            merged_components[component_name] = list(existing_map.values())
        
        # Generate state ID
        state_id = self._generate_state_id(merged_components)
        
        # Check if state already exists
        existing = self.redis.get(self._state_key(state_id))
        if existing:
            return state_id
        
        # Create state object
        state = State(
            state_id=state_id,
            api_slug=api_slug,
            parent_state_id=parent_state_id,
            action_path=action_path,
            modified_components=merged_components,
        )
        
        self._cache_state(state, add_parent_link=bool(parent_state_id))
        self._persist_state(state)
        
        print(f"[StateManager] Created state {state_id} for {api_slug}", file=sys.stderr)
        return state_id
    
    def get_state(self, state_id: str, reconstruct_if_missing: bool = True) -> State:
        """
        Get state from Redis.
        
        Args:
            state_id: State ID
            reconstruct_if_missing: If True, reconstruct state if evicted from cache
        
        Returns:
            State object
        """
        state_json = self.redis.get(self._state_key(state_id))
        
        if state_json:
            return json_to_model(State, state_json)
        
        # Cache miss - reconstruct if enabled
        if reconstruct_if_missing:
            print(f"[StateManager] Cache miss for {state_id}, reconstructing...", file=sys.stderr)
            return self.reconstruct_state(state_id)
        
        raise ValueError(f"State {state_id} not found in cache and reconstruction disabled")
    
    def reconstruct_state(self, state_id: str) -> State:
        """Reconstruct state from durable storage when cache misses."""
        if RLStateRecord is None or db_session is None:
            raise ValueError(
                f"State {state_id} not found in cache and no durable storage configured"
            )
        with db_session() as session:
            record = session.exec(
                select(RLStateRecord).where(RLStateRecord.state_id == state_id)
            ).first()
        if not record:
            raise ValueError(f"State {state_id} not found in durable store")
        state = State(
            state_id=record.state_id,
            api_slug=record.api_slug,
            parent_state_id=record.parent_state_id,
            action_path=list(record.action_path or []),
            modified_components=dict(record.modified_components or {}),
            created_at=record.created_at,
        )
        self._cache_state(state)
        return state

    def _cache_state(self, state: State, *, add_parent_link: bool = True) -> None:
        state_json = model_to_json(state)
        self.redis.set(self._state_key(state.state_id), state_json)
        self.redis.sadd(self._api_states_key(state.api_slug), state.state_id)
        if add_parent_link and state.parent_state_id:
            self.redis.sadd(self._state_children_key(state.parent_state_id), state.state_id)

    def _persist_state(self, state: State) -> None:
        if RLStateRecord is None or db_session is None:
            return
        with db_session() as session:
            existing = session.exec(
                select(RLStateRecord).where(RLStateRecord.state_id == state.state_id)
            ).first()
            if existing:
                existing.api_slug = state.api_slug
                existing.parent_state_id = state.parent_state_id
                existing.action_path = list(state.action_path)
                existing.modified_components = dict(state.modified_components)
            else:
                session.add(
                    RLStateRecord(
                        state_id=state.state_id,
                        api_slug=state.api_slug,
                        parent_state_id=state.parent_state_id,
                        action_path=list(state.action_path),
                        modified_components=dict(state.modified_components),
                    )
                )
    
    def detect_modified_components(
        self, api_slug: str, parent_state_id: Optional[str] = None
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Detect which components changed by comparing current DB state with parent state.
        
        Args:
            api_slug: API identifier
            parent_state_id: Parent state ID (None means compare with empty state)
        
        Returns:
            Dict of modified components: {component_name: [records]}
        """
        # Get current database state for all components
        # We need to get all component names for this API
        # For now, fetch all records and group by component
        current_components = {}
        
        # Get all records from database
        if runtime is None or db_session is None:
            raise RuntimeError("Runtime and database modules not available")
        
        with db_session() as session:
            records = session.exec(
                select(GeneratedRecord).where(GeneratedRecord.api_slug == api_slug)
            ).all()
            
            for record in records:
                component_name = record.component_name
                if component_name not in current_components:
                    current_components[component_name] = []
                current_components[component_name].append(record.payload)
        
        # Compare with parent state
        if parent_state_id:
            parent_state = self.get_state(parent_state_id, reconstruct_if_missing=True)
            parent_components = parent_state.modified_components
            
            # Find differences
            modified = {}
            for component_name, current_records in current_components.items():
                parent_records = parent_components.get(component_name, [])
                
                # Create maps for comparison
                current_map = {
                    str(r.get("id", r.get("record_key", ""))): r
                    for r in current_records
                }
                parent_map = {
                    str(r.get("id", r.get("record_key", ""))): r
                    for r in parent_records
                }
                
                # Check for changes
                changed = False
                for record_id, record in current_map.items():
                    if record_id not in parent_map or parent_map[record_id] != record:
                        changed = True
                        break
                
                # Check for deletions
                for record_id in parent_map:
                    if record_id not in current_map:
                        changed = True
                        break
                
                if changed:
                    modified[component_name] = current_records
        else:
            # No parent - all current components are modifications
            modified = current_components
        
        return modified
    
    def restore_state(self, state_id: str, initial_seed_data: Optional[Dict[str, List[Dict[str, Any]]]] = None) -> None:
        """
        Restore database to a specific state.
        
        Args:
            state_id: State to restore
            initial_seed_data: Initial seed data (if any) to start from
        """
        state = self.get_state(state_id, reconstruct_if_missing=True)
        
        # Start with seed data (or empty)
        if runtime is None:
            raise RuntimeError("Runtime module not available")
        
        if initial_seed_data:
            runtime.replace_dataset(state.api_slug, initial_seed_data)
        else:
            # Clear all records for this API
            runtime.remove_dataset(state.api_slug)
        
        # Apply modifications from state
        if state.modified_components:
            if runtime is None or db_session is None:
                raise RuntimeError("Runtime and database modules not available")
            
            # For each component, replace records
            for component_name, records in state.modified_components.items():
                # Clear existing records for this component
                with db_session() as session:
                    session.exec(
                        delete(GeneratedRecord)
                        .where(GeneratedRecord.api_slug == state.api_slug)
                        .where(GeneratedRecord.component_name == component_name)
                    )
                    
                    # Insert records
                    for record in records:
                        # Use runtime's _derive_record_key if available, otherwise simple key
                        if hasattr(runtime, '_derive_record_key'):
                            key = runtime._derive_record_key(record)
                        else:
                            key = str(record.get("id", record.get("record_key", "")))
                        
                        payload = dict(record)
                        if "id" not in payload:
                            payload["id"] = key
                        
                        session.add(
                            GeneratedRecord(
                                api_slug=state.api_slug,
                                component_name=component_name,
                                record_key=key,
                                payload=payload,
                            )
                        )
                    session.flush()
        
        print(f"[StateManager] Restored database to state {state_id}", file=sys.stderr)
    
    def get_initial_state(self, api_slug: str, seed_data: Optional[Dict[str, List[Dict[str, Any]]]] = None) -> str:
        """
        Get or create initial state (empty or with seed data).
        
        Args:
            api_slug: API identifier
            seed_data: Optional seed data
        
        Returns:
            state_id
        """
        # Initial state has empty modified_components
        initial_components = {}
        
        # If seed data provided, that becomes the initial state
        if seed_data:
            initial_components = seed_data
        
        state_id = self._generate_state_id(initial_components)
        
        # Check if exists
        existing = self.redis.get(self._state_key(state_id))
        if existing:
            return state_id
        
        # Create initial state
        state = State(
            state_id=state_id,
            api_slug=api_slug,
            parent_state_id=None,
            action_path=[],
            modified_components=initial_components,
        )
        
        self._cache_state(state, add_parent_link=False)
        self._persist_state(state)
        
        return state_id
    
    def get_state_children(self, state_id: str) -> List[str]:
        """Get all child state IDs."""
        children = self.redis.smembers(self._state_children_key(state_id))
        return list(children)
    
    def get_state_path(self, state_id: str) -> List[str]:
        """Get sequence of action IDs leading to this state."""
        state = self.get_state(state_id, reconstruct_if_missing=True)
        return state.action_path.copy()
