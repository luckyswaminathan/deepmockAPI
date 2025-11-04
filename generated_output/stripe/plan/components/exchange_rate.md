# Component Plan: `exchange_rate`

**API Slug:** `stripe`
**Total Routes:** 2

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.

## Routes

### GET Routes (2)

#### `GET /v1/exchange_rates`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `exchange_rate`
  - Notes:
    - Query parameters: ending_before, expand, limit, starting_after

#### `GET /v1/exchange_rates/{rate_id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `exchange_rate`
  - Filters:
    - `rate_id` eq `path.rate_id`
  - Notes:
    - Response body references #/components/schemas/exchange_rate
    - Query parameters: expand
