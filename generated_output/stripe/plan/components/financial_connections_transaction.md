# Component Plan: `financial_connections.transaction`

**API Slug:** `stripe`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /v1/financial_connections/transactions/{transaction}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `financial_connections.transaction`
  - Filters:
    - `transaction_refresh` eq `path.transaction`
  - Notes:
    - Response body references #/components/schemas/financial_connections.transaction
    - Query parameters: expand
