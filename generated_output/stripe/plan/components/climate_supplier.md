# Component Plan: `climate.supplier`

**API Slug:** `stripe`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /v1/climate/suppliers/{supplier}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `climate.supplier`
  - Filters:
    - `supplier` eq `path.supplier`
  - Notes:
    - Response body references #/components/schemas/climate.supplier
    - Query parameters: expand
