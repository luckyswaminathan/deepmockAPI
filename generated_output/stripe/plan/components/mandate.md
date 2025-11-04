# Component Plan: `mandate`

**API Slug:** `stripe`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /v1/mandates/{mandate}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `mandate`
  - Filters:
    - `mandate` eq `path.mandate`
  - Notes:
    - Response body references #/components/schemas/mandate
    - Query parameters: expand
