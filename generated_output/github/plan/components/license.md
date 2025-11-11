# Component Plan: `license`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /licenses/{license}`
**Summary:** Get a license
**Status:** planned

**Operations:**
- **read_one**
  - Component: `license`
  - Filters:
    - `license` eq `path.license`
  - Notes:
    - Response body references #/components/schemas/license
    - Query parameters: license
