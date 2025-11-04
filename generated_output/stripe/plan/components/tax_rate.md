# Component Plan: `tax_rate`

**API Slug:** `stripe`
**Total Routes:** 4

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.

## Routes

### GET Routes (2)

#### `GET /v1/tax_rates`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `tax_rate`
  - Notes:
    - Query parameters: active, created, ending_before, expand, inclusive, limit, starting_after

#### `GET /v1/tax_rates/{tax_rate}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `tax_rate`
  - Filters:
    - `tax_rate` eq `path.tax_rate`
  - Notes:
    - Response body references #/components/schemas/tax_rate
    - Query parameters: expand

### POST Routes (2)

#### `POST /v1/tax_rates`
**Status:** planned

**Operations:**
- **create**
  - Component: `tax_rate`
  - Notes:
    - Response body references #/components/schemas/tax_rate

#### `POST /v1/tax_rates/{tax_rate}`
**Status:** planned

**Operations:**
- **create**
  - Component: `tax_rate`
  - Filters:
    - `tax_rate` eq `path.tax_rate`
  - Notes:
    - Response body references #/components/schemas/tax_rate
    - Query parameters: tax_rate
