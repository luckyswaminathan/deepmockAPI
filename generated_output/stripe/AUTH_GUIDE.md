# Handling Authentication in Generated APIs

Some endpoints (like `/v1/balance`, `/v1/account`) depend on authentication context rather than simple database queries. This guide explains how to handle these auth-dependent endpoints in your generated mock API.

## Problem

The generated routes are stubs that assume simple CRUD operations. But some endpoints like:
- `/v1/balance` - Returns account balance based on authentication
- `/v1/account` - Returns the authenticated account
- `/v1/customers` - Returns customers for the authenticated account

These endpoints need to:
1. Extract authentication from the request (API keys, tokens)
2. Use that auth context to scope data retrieval
3. Return different data based on who's authenticated

## Solution: Auth Module

We've provided an `auth.py` module with helper functions:

### Basic Usage

```python
from auth import get_auth_context, get_account_id

@router.get("/v1/balance")
async def get_v1_balance() -> Any:
    # Get auth context (account_id, customer_id, mode)
    auth_context = get_auth_context()
    account_id = get_account_id(auth_context)
    
    # Use account-scoped storage
    balance = generated_runtime.fetch_account_component_records(
        account_id, "balance"
    )
    return balance[0] if balance else default_balance
```

### Authentication Support

The `auth.py` module supports:

1. **Bearer Token** (standard):
   ```bash
   curl -H "Authorization: Bearer sk_test_mock_default" \
     http://localhost:8000/v1/balance
   ```

2. **Stripe API Key Header**:
   ```bash
   curl -H "Stripe-Api-Key: sk_test_mock_default" \
     http://localhost:8000/v1/balance
   ```

3. **Optional Auth** (for development):
   - If no auth provided, uses default mock key
   - Allows testing without setting auth headers

### Mock API Keys

Default mock keys are defined in `auth.py`:

```python
_MOCK_API_KEYS = {
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
}
```

Add your own:
```python
from auth import add_mock_key

add_mock_key(
    api_key="sk_test_myapp",
    account_id="acct_myapp",
    customer_id="cus_myapp",
    mode="test"
)
```

## Account-Scoped Storage

The runtime now supports account-scoped storage for auth-dependent endpoints:

```python
# Store data scoped to an account
generated_runtime.insert_account_component_record(
    account_id="acct_123",
    component_name="balance",
    payload={"available": [{"amount": 1000, "currency": "usd"}]}
)

# Fetch data scoped to an account
balance = generated_runtime.fetch_account_component_records(
    account_id="acct_123",
    component_name="balance"
)
```

## Patterns for Different Endpoint Types

### 1. Auth-Dependent (Account Context)

Endpoints that return data for the authenticated account:

```python
@router.get("/v1/balance")
async def get_v1_balance() -> Any:
    auth_context = get_auth_context()
    account_id = get_account_id(auth_context)
    
    # Use account-scoped storage
    balance = generated_runtime.fetch_account_component_records(
        account_id, "balance"
    )
    
    if not balance:
        # Return default or compute from transactions
        return default_balance_structure()
    
    return balance[0]
```

### 2. Optional Auth (Fallback to Default)

Endpoints that work with or without auth:

```python
@router.get("/v1/account")
async def get_v1_account() -> Any:
    auth_context = get_auth_context()  # Uses default if missing
    account_id = get_account_id(auth_context)
    
    account = generated_runtime.fetch_component_record(
        "stripe", "account", "id", account_id
    )
    
    return account or default_account()
```

### 3. Required Auth (Strict)

Endpoints that must have authentication:

```python
from auth import require_auth

@router.get("/v1/secret_endpoint")
async def get_v1_secret_endpoint() -> Any:
    # Raises 401 if no valid auth
    auth_context = require_auth()
    account_id = get_account_id(auth_context)
    
    # Your logic here
    return {"account_id": account_id}
```

### 4. Customer-Scoped

Endpoints scoped to a customer:

```python
@router.get("/v1/customers/{customer_id}/subscriptions")
async def get_subscriptions(*, customer_id: str) -> Any:
    auth_context = get_auth_context()
    auth_customer_id = auth_context.get("customer_id")
    
    # Optionally validate ownership
    if auth_customer_id and customer_id != auth_customer_id:
        # Could validate account_id match instead
        pass
    
    # Fetch subscriptions for this customer
    subscriptions = generated_runtime.fetch_component_records(
        "stripe", "subscription"
    )
    
    # Filter to customer
    customer_subs = [s for s in subscriptions if s.get("customer") == customer_id]
    
    return {"data": customer_subs}
```

## Dynamic Balance Calculation

For endpoints like `/v1/balance`, you might want to compute values dynamically:

```python
@router.get("/v1/balance")
async def get_v1_balance() -> Any:
    auth_context = get_auth_context()
    account_id = get_account_id(auth_context)
    
    # Fetch transactions
    transactions = generated_runtime.fetch_account_component_records(
        account_id, "balance_transaction"
    )
    
    # Calculate available balance
    available_amount = sum(
        t.get("amount", 0) 
        for t in transactions 
        if t.get("status") == "available"
    )
    
    # Calculate pending balance
    pending_amount = sum(
        t.get("amount", 0) 
        for t in transactions 
        if t.get("status") == "pending"
    )
    
    balance = {
        "object": "balance",
        "available": [{"amount": available_amount, "currency": "usd"}],
        "pending": [{"amount": pending_amount, "currency": "usd"}],
        "livemode": False,
    }
    
    # Cache it
    generated_runtime.insert_account_component_record(
        account_id, "balance", balance
    )
    
    return balance
```

## Testing with Different Accounts

```python
# Test with default account
curl http://localhost:8000/v1/balance

# Test with specific account
curl -H "Authorization: Bearer sk_test_mock_account2" \
  http://localhost:8000/v1/balance

# Test with Stripe API key format
curl -H "Stripe-Api-Key: sk_test_mock_account2" \
  http://localhost:8000/v1/balance
```

## Production Considerations

For production use:

1. **Replace Mock Auth**: Replace `auth.py` with real authentication logic
2. **Validate API Keys**: Validate against real Stripe API keys or your own auth service
3. **Account Isolation**: Ensure strict account isolation in data storage
4. **Rate Limiting**: Add rate limiting per API key
5. **Token Expiry**: Handle token expiration if using JWT/OAuth

Example production auth:
```python
from authlib.jose import jwt
from your_auth_service import validate_api_key

def get_auth_context(token: str = None) -> dict:
    if not token:
        raise HTTPException(401, "Authentication required")
    
    # Validate token against auth service
    account_info = validate_api_key(token)
    if not account_info:
        raise HTTPException(401, "Invalid API key")
    
    return account_info
```

## See Also

- `examples_balance_endpoint.py` - Working examples
- `auth.py` - Auth helper module
- `runtime.py` - Storage with account-scoped operations

