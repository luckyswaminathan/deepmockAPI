"""Authentication and authorization helpers for the Stripe API mock.

This module provides mock authentication for development/testing purposes.
In production, replace with real authentication logic.
"""

from __future__ import annotations

from typing import Optional
from fastapi import Header, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


# Mock authentication token storage
# In production, this would validate against a real auth service
_MOCK_API_KEYS: dict[str, dict[str, str]] = {
    # Example mock API key -> account mapping
    "sk_test_mock_default": {
        "account_id": "acct_default",
        "customer_id": "cus_default",
        "mode": "test",
    },
    "sk_test_mock_account2": {
        "account_id": "acct_123456",
        "customer_id": "cus_123456",
        "mode": "test",
    },
    "sk_live_mock_production": {
        "account_id": "acct_production",
        "customer_id": "cus_production",
        "mode": "live",
    },
}

# For development: allow optional auth (defaults to first mock key)
_DEFAULT_KEY = "sk_test_mock_default"

security = HTTPBearer(auto_error=False)


def get_auth_context(
    authorization: Optional[HTTPAuthorizationCredentials] = Security(security),
    stripe_api_key: Optional[str] = Header(None, alias="Stripe-Api-Key"),
) -> dict[str, str]:
    """
    Extract authentication context from request.
    
    Supports both:
    - Bearer token in Authorization header
    - Stripe-Api-Key header (Stripe's format)
    
    Returns a dict with account/customer context.
    If no auth provided, uses default mock key for development.
    """
    # Try Authorization header first
    token = None
    if authorization:
        token = authorization.credentials
    
    # Fall back to Stripe-Api-Key header
    if not token and stripe_api_key:
        token = stripe_api_key
    
    # For development: use default if no auth provided
    if not token:
        token = _DEFAULT_KEY
    
    # Look up auth context
    auth_context = _MOCK_API_KEYS.get(token)
    
    if not auth_context:
        # In production, you might want to raise 401 here
        # For mock, return default context
        auth_context = _MOCK_API_KEYS[_DEFAULT_KEY]
    
    return auth_context.copy()


def require_auth(
    authorization: Optional[HTTPAuthorizationCredentials] = Security(security),
    stripe_api_key: Optional[str] = Header(None, alias="Stripe-Api-Key"),
) -> dict[str, str]:
    """
    Require valid authentication, raise 401 if missing.
    
    Use this for endpoints that absolutely require auth.
    """
    token = None
    if authorization:
        token = authorization.credentials
    
    if not token and stripe_api_key:
        token = stripe_api_key
    
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Authentication required. Provide 'Authorization: Bearer <token>' or 'Stripe-Api-Key' header.",
        )
    
    auth_context = _MOCK_API_KEYS.get(token)
    
    if not auth_context:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid API key: {token[:20]}...",
        )
    
    return auth_context.copy()


def get_account_id(auth_context: dict[str, str]) -> str:
    """Get the account ID from auth context."""
    return auth_context.get("account_id", "acct_default")


def get_customer_id(auth_context: dict[str, str]) -> Optional[str]:
    """Get the customer ID from auth context (if available)."""
    return auth_context.get("customer_id")


def add_mock_key(api_key: str, account_id: str, customer_id: Optional[str] = None, mode: str = "test") -> None:
    """
    Add a mock API key for testing.
    
    Example:
        add_mock_key("sk_test_myapp", "acct_myapp", "cus_myapp", "test")
    """
    _MOCK_API_KEYS[api_key] = {
        "account_id": account_id,
        "customer_id": customer_id or f"cus_{account_id.split('_')[-1]}",
        "mode": mode,
    }

