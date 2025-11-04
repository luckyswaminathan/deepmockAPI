# Component Plan: `issuing.physical_bundle`

**API Slug:** `stripe`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /v1/issuing/physical_bundles/{physical_bundle}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `issuing.physical_bundle`
  - Filters:
    - `physical_bundle` eq `path.physical_bundle`
  - Notes:
    - Response body references #/components/schemas/issuing.physical_bundle
    - Query parameters: expand
