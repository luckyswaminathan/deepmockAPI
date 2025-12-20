"""Action Masker for determining valid actions at each state."""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Set

from .models import State
from .state_manager import StateManager


class ActionMasker:
    """Determines which actions are valid at a given state."""
    
    def __init__(self, state_manager: StateManager):
        self.state_manager = state_manager
    
    def get_valid_actions(
        self,
        state_id: str,
        available_actions: List[Dict[str, Any]],
    ) -> List[str]:
        """
        Get list of valid action IDs at the current state.
        
        Args:
            state_id: Current state ID
            available_actions: List of available actions, each with:
                - action_id (or method+path used as ID)
                - method: HTTP method
                - path: API path (may contain {id} placeholders)
                - body: Optional request body template
        
        Returns:
            List of valid action IDs (or method+path strings)
        """
        state = self.state_manager.get_state(state_id, reconstruct_if_missing=True)
        
        # Extract known IDs from state
        known_ids = self._extract_known_ids(state.modified_components)
        
        # Extract component types that exist
        existing_components = set(state.modified_components.keys())
        
        valid_action_ids = []
        
        for action in available_actions:
            action_id = action.get("action_id") or f"{action.get('method')}:{action.get('path')}"
            
            if self._is_action_valid(action, known_ids, existing_components):
                valid_action_ids.append(action_id)
        
        return valid_action_ids
    
    def _is_action_valid(
        self,
        action: Dict[str, Any],
        known_ids: Dict[str, List[str]],
        existing_components: Set[str],
    ) -> bool:
        """
        Check if an action is valid given current state.
        
        Rules:
        - POST /{component}s: valid if component doesn't exist yet (or always valid)
        - GET/PUT/PATCH/DELETE /{component}s/{id}: valid only if component exists and ID is known
        - Templated routes: valid only if all required IDs exist
        """
        method = action.get("method", "").upper()
        path = action.get("path", "")
        
        # Extract component name from path
        component = self._extract_component_from_path(path)
        
        # Check for path parameters (e.g., {id}, {customer_id})
        path_params = self._extract_path_params(path)
        
        # POST to collection endpoint: usually valid (creating new resource)
        if method == "POST" and not path_params:
            return True
        
        # For templated routes, check if all required IDs exist
        if path_params:
            for param in path_params:
                # Map parameter name to component type
                param_component = self._param_to_component(param)
                
                # Check if we have IDs for this component
                if param_component not in known_ids or not known_ids[param_component]:
                    return False
        
        # For GET/PUT/PATCH/DELETE on specific resources, component should exist
        if method in ("GET", "PUT", "PATCH", "DELETE") and component:
            # If it's a collection endpoint (no ID), it's usually valid
            if not path_params:
                return True
            
            # If it's a specific resource, check if component exists
            if component not in existing_components:
                return False
        
        # Default: allow if no obvious reason to block
        return True
    
    def _extract_component_from_path(self, path: str) -> Optional[str]:
        """Extract component name from API path."""
        # Remove leading/trailing slashes and split
        parts = [p for p in path.strip("/").split("/") if p and not p.startswith("{")]
        
        if not parts:
            return None
        
        # Get the last resource name (before any {id} parts)
        resource = parts[-1]
        
        # Convert plural to singular (simple heuristic)
        if resource.endswith("ies"):
            component = resource[:-3] + "y"
        elif resource.endswith("s") and len(resource) > 1:
            component = resource[:-1]
        else:
            component = resource
        
        # Convert to snake_case
        component = component.replace("-", "_").lower()
        
        return component
    
    def _extract_path_params(self, path: str) -> List[str]:
        """Extract path parameter names from a path (e.g., {id}, {customer_id})."""
        pattern = r"\{([^}]+)\}"
        matches = re.findall(pattern, path)
        return matches
    
    def _param_to_component(self, param: str) -> str:
        """
        Map a path parameter name to a component type.
        
        Examples:
            id -> generic (use context)
            customer_id -> customer
            invoice_id -> invoice
        """
        # Remove common suffixes
        param = param.lower().replace("_id", "").replace("id", "")
        
        # If empty after removing id, it's a generic ID (use context)
        if not param:
            return "generic"
        
        return param
    
    def _extract_known_ids(
        self,
        modified_components: Dict[str, List[Dict[str, Any]]],
    ) -> Dict[str, List[str]]:
        """Extract known entity IDs by component type."""
        known_ids = {}
        
        for component_name, records in modified_components.items():
            ids = []
            for record in records:
                # Try to extract ID from common fields
                record_id = (
                    record.get("id") or
                    record.get("record_key") or
                    record.get("_id")
                )
                if record_id:
                    ids.append(str(record_id))
            
            if ids:
                known_ids[component_name] = ids
        
        return known_ids

