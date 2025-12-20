"""FastAPI middleware for automatic RL action tracking."""

from __future__ import annotations

import json
import sys
from typing import Optional

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import StreamingResponse
from starlette.types import Message

from .action_tracker import ActionTracker
from .redis_client import get_redis_client
from .state_manager import StateManager


class RLMiddleware(BaseHTTPMiddleware):
    """
    Middleware to automatically track API actions for RL.
    
    Tracks requests to /generated/{api_slug}/* routes and records them as actions.
    Supports state restoration via X-RL-State-Id header.
    """
    
    def __init__(self, app, enabled: bool = True):
        super().__init__(app)
        self.enabled = enabled
        self.state_manager = StateManager()
        self.action_tracker = ActionTracker(self.state_manager)
        self.redis = get_redis_client()
    
    async def dispatch(self, request: Request, call_next):
        """Process request and track actions."""
        if not self.enabled:
            return await call_next(request)
        
        # Only track generated API routes
        # Use scope["path"] directly to handle internal ASGI requests (no URL scheme)
        try:
            path = request.url.path
        except (KeyError, AttributeError):
            # Fallback for internal ASGI requests without URL scheme
            path = request.scope.get("path", "")
        
        if not path.startswith("/generated/"):
            return await call_next(request)
        
        # Extract API slug from path: /generated/{api_slug}/...
        parts = path.split("/")
        if len(parts) < 3:
            return await call_next(request)
        
        api_slug = parts[2]
        
        # Check for state restoration header
        restore_state_id = request.headers.get("X-RL-State-Id")
        if restore_state_id:
            try:
                self.state_manager.restore_state(restore_state_id)
                print(f"[RLMiddleware] Restored state {restore_state_id} for {api_slug}", file=sys.stderr)
                # IMPORTANT: Use the restored state as current_state_id, not session state
                # This ensures each action starts from the specified state (e.g., start state)
                current_state_id = restore_state_id
            except Exception as e:
                print(f"[RLMiddleware] Failed to restore state {restore_state_id}: {e}", file=sys.stderr)
                current_state_id = None
        else:
            current_state_id = None
        
        # Get or create session for automatic tracking
        session_id = request.headers.get("X-RL-Session-Id")
        
        # Only use session state if we didn't restore from header
        if current_state_id is None:
            if session_id:
                # Use provided session
                current_state_id = self._get_session_current_state(session_id)
            else:
                # Auto-create anonymous session for this API
                session_id = self._get_or_create_api_session(api_slug)
                current_state_id = self._get_session_current_state(session_id)
            
            # If still no state, create initial state for this API
            if not current_state_id:
                current_state_id = self.state_manager.get_initial_state(api_slug)
                # Update session with initial state
                self._update_session_state(session_id, current_state_id, None)
        
        # Extract request data
        method = request.method
        path_params = dict(request.path_params)
        query_params = dict(request.query_params)
        params = {**path_params, **query_params}
        
        # Read request body if present
        request_body = None
        if method in ("POST", "PUT", "PATCH"):
            try:
                body_bytes = await request.body()
                if body_bytes:
                    request_body = json.loads(body_bytes)
            except (json.JSONDecodeError, ValueError):
                pass
        
        # Execute request and capture response
        response = await call_next(request)
        
        # Extract response data
        response_status = response.status_code
        response_body = None
        
        # Priority 1: Capture response body properly
        # Note: We can't easily capture streaming response bodies without blocking
        # For now, we'll rely on database state detection for tracking changes
        # Response body capture would require a more complex streaming wrapper
        # that's not compatible with FastAPI's async response handling
        
        # Try to read response body if it's a simple response (not streaming)
        # Most FastAPI responses return JSON which we can't easily intercept
        # without breaking the streaming mechanism
        
        # Priority 3: Extract component name from route metadata
        # Try to get component from route's docstring or metadata
        component_name = self._extract_component_from_route(request, path, method)
        
        # Record action (async, don't block response)
        # Note: response_body is None - we rely on database state detection
        # This is more reliable than trying to capture streaming response bodies
        try:
            action_id, next_state_id = self.action_tracker.record_action(
                state_id=current_state_id,
                method=method,
                path=path,
                params=params,
                request_body=request_body,
                response_status=response_status,
                response_body=response_body,  # None - using DB detection instead
                component_name=component_name,  # From route metadata
            )
            
            # Update session current state
            if session_id:
                self._update_session_state(session_id, next_state_id, action_id)
            
            # Add headers to response
            response.headers["X-RL-Action-Id"] = action_id
            response.headers["X-RL-Next-State-Id"] = next_state_id
            
        except Exception as e:
            print(f"[RLMiddleware] Failed to record action: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc(file=sys.stderr)
        
        return response
    
    def _get_session_current_state(self, session_id: str) -> Optional[str]:
        """Get current state ID from session."""
        try:
            session_json = self.redis.get(f"session:{session_id}")
            if session_json:
                session_data = json.loads(session_json)
                return session_data.get("current_state_id")
        except Exception:
            pass
        return None
    
    def _get_or_create_api_session(self, api_slug: str) -> str:
        """Get or create an anonymous session for an API."""
        # Use a per-API session key: api_session:{api_slug}
        session_key = f"api_session:{api_slug}"
        session_id = self.redis.get(session_key)
        
        if not session_id:
            # Create new session
            from uuid import uuid4
            from datetime import datetime
            session_id = f"session_{uuid4().hex[:16]}"
            session_data = {
                "session_id": session_id,
                "api_slug": api_slug,
                "current_state_id": None,
                "start_state_id": None,
                "actions": [],
                "created_at": datetime.utcnow().isoformat(),
            }
            self.redis.set(f"session:{session_id}", json.dumps(session_data))
            # Store session ID for this API
            self.redis.set(session_key, session_id)
        
        return session_id
    
    def _update_session_state(self, session_id: str, state_id: str, action_id: Optional[str] = None) -> None:
        """Update session with new state and action."""
        try:
            session_json = self.redis.get(f"session:{session_id}")
            if session_json:
                session_data = json.loads(session_json)
                session_data["current_state_id"] = state_id
                if session_data.get("start_state_id") is None:
                    session_data["start_state_id"] = state_id
                session_data["action_history"] = session_data.get("action_history", [])
                if action_id:
                    session_data["action_history"].append(action_id)
                self.redis.set(f"session:{session_id}", json.dumps(session_data))
            else:
                # Create session if it doesn't exist (shouldn't happen, but handle it)
                from datetime import datetime
                session_data = {
                    "session_id": session_id,
                    "api_slug": "unknown",  # API slug not available here
                    "current_state_id": state_id,
                    "start_state_id": state_id,
                    "actions": [action_id] if action_id else [],
                    "created_at": datetime.utcnow().isoformat(),
                }
                self.redis.set(f"session:{session_id}", json.dumps(session_data))
        except Exception as e:
            print(f"[RLMiddleware] Failed to update session: {e}", file=sys.stderr)
    
    def _extract_component_from_route(self, request: Request, path: str, method: str) -> Optional[str]:
        """
        Priority 3: Extract component name from route metadata.
        
        Tries to get component from:
        1. Route's docstring (e.g., "Target component: account")
        2. Route function metadata
        3. Falls back to path inference
        """
        try:
            # Try to get the route handler from request
            # FastAPI stores route info in request.scope
            route = request.scope.get("route")
            if route:
                # Try to get the endpoint function
                endpoint = getattr(route, "endpoint", None)
                if endpoint:
                    # Check docstring for component
                    doc = getattr(endpoint, "__doc__", None)
                    if doc:
                        # Look for "Target component: {name}" pattern
                        import re
                        match = re.search(r"Target component:\s*(\w+)", doc)
                        if match:
                            return match.group(1)
                    
                    # Check function annotations or metadata
                    # Some routes might have component in metadata
                    if hasattr(endpoint, "__annotations__"):
                        # Could check for component annotation
                        pass
        except Exception:
            # If extraction fails, return None (will use path inference)
            pass
        
        # Fallback: return None, let action_tracker infer from path
        return None

