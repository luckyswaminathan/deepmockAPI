# Component Plan: `tax.calculation`

**API Slug:** `stripe`
**Total Routes:** 2

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /v1/tax/calculations/{calculation}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `tax.calculation`
  - Filters:
    - `calculation` eq `path.calculation`
  - Notes:
    - Response body references #/components/schemas/tax.calculation
    - Query parameters: expand

### POST Routes (1)

#### `POST /v1/tax/calculations`
**Status:** planned

**Operations:**
- **create**
  - Component: `tax.calculation`
  - Notes:
    - Response body references #/components/schemas/tax.calculation
