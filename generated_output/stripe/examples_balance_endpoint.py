"""Example: How to handle auth-dependent endpoints like /v1/balance

This shows how to modify the generated routes.py to handle endpoints
that depend on authentication context rather than just database queries.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

# Import runtime (existing)
import sys
from pathlib import Path
parent_dir = str(Path(__file__).parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import runtime as generated_runtime
from auth import get_auth_context, get_account_id

router = APIRouter()

# Example 1: Balance endpoint - depends on authenticated account
@router.get("/v1/balance")
async def get_v1_balance() -> Any:
    """
    Get balance for the authenticated account.
    
    This endpoint depends on authentication - it returns different data
    based on which API key was used to authenticate.
    """
    # Get auth context (account_id, customer_id, etc.)
    auth_context = get_auth_context()
    account_id = get_account_id(auth_context)
    
    # Option A: Use account-scoped storage
    # Fetch balance records scoped to this account
    balance_records = generated_runtime.fetch_account_component_records(
        account_id, "balance"
    )
    
    if balance_records:
        # Return the first balance record for this account
        return balance_records[0]
    
    # Option B: Compute balance from transactions
    # If you want dynamic balance calculation:
    transactions = generated_runtime.fetch_account_component_records(
        account_id, "balance_transaction"
    )
    
    # Calculate balance from transactions
    balance = {
        "object": "balance",
        "available": [{"amount": sum(t.get("amount", 0) for t in transactions), "currency": "usd"}],
        "connect_reserved": [],
        "instant_available": [],
        "issuing": {},
        "livemode": False,
        "pending": [],
    }
    
    # Store it for future requests
    generated_runtime.insert_account_component_record(
        account_id, "balance", balance
    )
    
    return balance


# Example 2: Endpoint with optional auth (falls back to default)
@router.get("/v1/account")
async def get_v1_account() -> Any:
    """
    Get account - can work with or without auth.
    """
    auth_context = get_auth_context()  # Uses default if no auth provided
    account_id = get_account_id(auth_context)
    
    # Fetch account by ID
    account = generated_runtime.fetch_component_record(
        "stripe", "account", "id", account_id
    )
    
    if not account:
        # Return a default account structure
        account = {
            "id": account_id,
            "object": "account",
            "charges_enabled": True,
            "country": "US",
            "default_currency": "usd",
            "details_submitted": True,
            "payouts_enabled": True,
            "type": "standard",
        }
    
    return account


# Example 3: Endpoint that requires auth
@router.get("/v1/connect_accounts")
async def get_v1_connect_accounts() -> Any:
    """
    Get connected accounts - requires authentication.
    """
    from auth import require_auth
    
    # This will raise 401 if no valid auth provided
    auth_context = require_auth()
    account_id = get_account_id(auth_context)
    
    # Fetch accounts connected to this account
    # In real Stripe, this would be Connect accounts
    connected_accounts = generated_runtime.fetch_account_component_records(
        account_id, "account"
    )
    
    return {
        "object": "list",
        "data": connected_accounts,
        "has_more": False,
        "url": "/v1/accounts",
    }


# Example 4: Customer-scoped endpoint
@router.get("/v1/customers/{customer_id}")
async def get_v1_customers(*, customer_id: str) -> Any:
    """
    Get customer - validate it belongs to authenticated account if auth provided.
    """
    auth_context = get_auth_context()
    auth_account_id = get_account_id(auth_context)
    auth_customer_id = auth_context.get("customer_id")
    
    # Fetch customer
    customer = generated_runtime.fetch_component_record(
        "stripe", "customer", "id", customer_id
    )
    
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found.")
    
    # If auth is provided, optionally validate ownership
    # (Skip validation if no auth - for development/testing)
    if auth_customer_id and customer_id != auth_customer_id:
        # In production, might want stricter validation
        # For mock, allow but could add account_id validation
        pass
    
    return customer

