# Component Plan: `balance_transaction`

**API Slug:** `stripe`
**Total Routes:** 4

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.

## Routes

### GET Routes (4)

#### `GET /v1/balance/history/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `balance_transaction`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/balance_transaction
    - Query parameters: expand

#### `GET /v1/balance_transactions`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `balance_transaction`
  - Notes:
    - Query parameters: created, currency, ending_before, expand, limit, payout, source, starting_after, type

#### `GET /v1/balance_transactions/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `balance_transaction`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/balance_transaction
    - Query parameters: expand

#### `GET /v1/customers/{customer}/balance_transactions`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `balance_transaction`
  - Filters:
    - `customer` eq `path.customer`
  - Notes:
    - Query parameters: ending_before, expand, limit, starting_after
