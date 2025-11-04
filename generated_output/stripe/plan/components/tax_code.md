# Component Plan: `tax_code`

**API Slug:** `stripe`
**Total Routes:** 2

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.

## Routes

### GET Routes (2)

#### `GET /v1/tax_codes`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `tax_code`
  - Notes:
    - Query parameters: ending_before, expand, limit, starting_after

#### `GET /v1/tax_codes/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `tax_code`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/tax_code
    - Query parameters: expand
