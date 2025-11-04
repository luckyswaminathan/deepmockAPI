# Component Plan: `code-of-conduct`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /codes_of_conduct/{key}`
**Summary:** Get a code of conduct
**Status:** planned

**Operations:**
- **read_one**
  - Component: `code-of-conduct`
  - Filters:
    - `key` eq `path.key`
  - Notes:
    - Response body references #/components/schemas/code-of-conduct
    - Query parameters: key
