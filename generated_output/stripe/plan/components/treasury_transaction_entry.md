# Component Plan: `treasury.transaction_entry`

**API Slug:** `stripe`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /v1/treasury/transaction_entries/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `treasury.transaction_entry`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/treasury.transaction_entry
    - Query parameters: expand
