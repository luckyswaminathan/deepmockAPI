# Component Plan: `country_spec`

**API Slug:** `stripe`
**Total Routes:** 2

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.

## Routes

### GET Routes (2)

#### `GET /v1/country_specs`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `country_spec`
  - Notes:
    - Query parameters: ending_before, expand, limit, starting_after

#### `GET /v1/country_specs/{country}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `country_spec`
  - Filters:
    - `country` eq `path.country`
  - Notes:
    - Response body references #/components/schemas/country_spec
    - Query parameters: expand
