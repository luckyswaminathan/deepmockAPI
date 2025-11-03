# How Authentication Works - Step by Step

This explains how the auth system works for endpoints like `/v1/balance` that depend on authentication.

## The Problem

Some endpoints need to return **different data based on who's authenticated**:

- `/v1/balance` → Should return balance for the authenticated account
- `/v1/account` → Should return the authenticated account's info
- `/v1/customers` → Should return customers for the authenticated account

Without auth, everyone sees the same data. With auth, each account sees only their own data.

## Step-by-Step Flow

### 1. Client Makes Request

```bash
# Example: Get balance with API key
curl -H "Authorization: Bearer sk_test_mock_account2" \
  http://localhost:8000/v1/balance
```

**Request Headers:**
```
Authorization: Bearer sk_test_mock_account2
```

### 2. FastAPI Route Handler

The route receives the request:

```python
@router.get("/v1/balance")
async def get_v1_balance() -> Any:
    # Step 3: Extract auth context
    auth_context = get_auth_context()
    account_id = get_account_id(auth_context)
    
    # Step 4: Fetch account-specific data
    balance = generated_runtime.fetch_account_component_records(
        account_id, "balance"
    )
    
    return balance[0] if balance else default_balance
```

### 3. `get_auth_context()` - Extract Auth Info

This function runs **automatically** when called (FastAPI dependency injection):

```python
def get_auth_context(
    authorization: Optional[HTTPAuthorizationCredentials] = Security(security),
    stripe_api_key: Optional[str] = Header(None, alias="Stripe-Api-Key"),
) -> dict[str, str]:
```

**What happens:**

1. **Check Authorization header:**
   ```python
   if authorization:
       token = authorization.credentials  # Gets "sk_test_mock_account2"
   ```

2. **Fallback to Stripe-Api-Key header:**
   ```python
   if not token and stripe_api_key:
       token = stripe_api_key
   ```

3. **Default for development (optional):**
   ```python
   if not token:
       token = "sk_test_mock_default"  # Uses default for testing
   ```

4. **Look up in mock API keys:**
   ```python
   auth_context = _MOCK_API_KEYS.get(token)
   # Returns: {"account_id": "acct_123456", "customer_id": "cus_123456", "mode": "test"}
   ```

### 4. Account-Scoped Storage

Now we have `account_id = "acct_123456"`. Use it to fetch account-specific data:

```python
balance = generated_runtime.fetch_account_component_records(
    account_id="acct_123456", 
    component_name="balance"
)
```

**Storage Structure:**
```python
_account_storage = {
    "acct_default": {
        "balance": [{"available": [{"amount": 1000, "currency": "usd"}]}],
        "balance_transaction": [...],
    },
    "acct_123456": {
        "balance": [{"available": [{"amount": 5000, "currency": "usd"}]}],
        "balance_transaction": [...],
    },
    "acct_production": {
        "balance": [{"available": [{"amount": 10000, "currency": "usd"}]}],
    },
}
```

**Result:** Each account gets **isolated data**. Account `acct_123456` only sees their balance of $50, not $10 or $100.

### 5. Return Response

The route returns account-specific data:
```json
{
  "object": "balance",
  "available": [{"amount": 5000, "currency": "usd"}],
  "livemode": false
}
```

## Complete Example Flow

```
┌─────────────┐
│   Client    │
│             │
│ Sends:      │
│ GET /v1/balance
│ Header: Authorization: Bearer sk_test_account2
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  FastAPI Route  │
│                 │
│ @router.get()   │
│ def balance()   │
└──────┬──────────┘
       │
       │ Calls: auth_context = get_auth_context()
       ▼
┌──────────────────┐
│  get_auth_context│
│                  │
│ 1. Extract token │
│    from header   │
│                  │
│ 2. Lookup token  │
│    in API keys   │
│                  │
│ 3. Return:       │
│    account_id    │
│    customer_id   │
└──────┬───────────┘
       │
       │ Returns: {"account_id": "acct_123"}
       ▼
┌──────────────────────┐
│  Route Handler        │
│                       │
│ account_id = "acct_123"│
│                       │
│ Calls:                │
│ runtime.fetch_account_│
│ component_records()   │
└──────┬─────────────────┘
       │
       │ Fetches from _account_storage["acct_123"]["balance"]
       ▼
┌──────────────────┐
│ Account Storage  │
│                  │
│ acct_123: {      │
│   balance: [...] │
│ }                │
└──────┬───────────┘
       │
       │ Returns account-specific balance
       ▼
┌──────────────────┐
│  Response        │
│                  │
│ {"available":    │
│   [{"amount": 5000│
│      }]          │
│ }                │
└──────────────────┘
```

## Real Example

Let's trace through a real request:

### Request
```bash
curl -H "Authorization: Bearer sk_test_mock_account2" \
  http://localhost:8000/v1/balance
```

### Step-by-Step

1. **Request arrives** with header `Authorization: Bearer sk_test_mock_account2`

2. **Route handler calls** `get_auth_context()`

3. **Auth function processes:**
   ```python
   token = "sk_test_mock_account2"  # Extracted from header
   
   # Lookup in mock keys
   _MOCK_API_KEYS["sk_test_mock_account2"]
   # Returns: {
   "account_id": "acct_123456",
   "customer_id": "cus_123456", 
   "mode": "test"
   }
   ```

4. **Route gets:** `account_id = "acct_123456"`

5. **Fetch data:**
   ```python
   balance = fetch_account_component_records(
       account_id="acct_123456",
       component_name="balance"
   )
   # Looks in: _account_storage["acct_123456"]["balance"]
   # Returns: [{"available": [{"amount": 5000}]}]
   ```

6. **Response:**
   ```json
   {
     "object": "balance",
     "available": [{"amount": 5000, "currency": "usd"}]
   }
   ```

## Different Accounts, Different Data

**Request 1:**
```bash
curl -H "Authorization: Bearer sk_test_mock_default" \
  http://localhost:8000/v1/balance
```
→ Account: `acct_default` → Balance: `$1,000`

**Request 2:**
```bash
curl -H "Authorization: Bearer sk_test_mock_account2" \
  http://localhost:8000/v1/balance
```
→ Account: `acct_123456` → Balance: `$5,000`

**Same endpoint, different data based on authentication!**

## Key Concepts

### 1. **Token → Account Mapping**
```
sk_test_mock_default    → acct_default
sk_test_mock_account2   → acct_123456  
sk_live_mock_production → acct_production
```

### 2. **Account-Scoped Storage**
Data is stored per account:
```python
_account_storage[account_id][component_name] = [records...]
```

### 3. **Auth Context**
Once authenticated, you get:
```python
{
  "account_id": "acct_123456",  # Used for data isolation
  "customer_id": "cus_123456",  # Optional customer context
  "mode": "test"                 # test/live mode
}
```

## Adding Test Data

To seed different balances for different accounts:

```python
from runtime import insert_account_component_record

# Account 1 balance
insert_account_component_record(
    account_id="acct_default",
    component_name="balance",
    payload={
        "available": [{"amount": 1000, "currency": "usd"}],
        "pending": [{"amount": 200, "currency": "usd"}],
    }
)

# Account 2 balance
insert_account_component_record(
    account_id="acct_123456",
    component_name="balance",
    payload={
        "available": [{"amount": 5000, "currency": "usd"}],
        "pending": [{"amount": 500, "currency": "usd"}],
    }
)
```

## Summary

**The Flow:**
1. **Request** includes auth token (Bearer or Stripe-Api-Key header)
2. **Extract** token from headers
3. **Lookup** token → account_id mapping
4. **Fetch** data scoped to that account_id
5. **Return** account-specific response

**Key Benefit:** Each authenticated account sees only their own data, just like a real API!

