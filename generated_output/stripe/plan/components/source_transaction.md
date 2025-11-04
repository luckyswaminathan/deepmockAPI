# Component Plan: `source_transaction`

**API Slug:** `stripe`
**Total Routes:** 2

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (2)

#### `GET /v1/sources/{source}/source_transactions`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `source_transaction`
  - Filters:
    - `source` eq `path.source`
  - Notes:
    - Query parameters: ending_before, expand, limit, starting_after

#### `GET /v1/sources/{source}/source_transactions/{source_transaction}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `source_transaction`
  - Filters:
    - `source` eq `path.source`
    - `source_transaction` eq `path.source_transaction`
  - Notes:
    - Response body references #/components/schemas/source_transaction
    - Query parameters: expand
