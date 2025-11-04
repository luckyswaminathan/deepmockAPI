# Component Plan: `treasury.transaction`

**API Slug:** `stripe`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /v1/treasury/transactions/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `treasury.transaction`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/treasury.transaction
    - Query parameters: expand
