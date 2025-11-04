# Component Plan: `gitignore-template`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /gitignore/templates/{name}`
**Summary:** Get a gitignore template
**Status:** planned

**Operations:**
- **read_one**
  - Component: `gitignore-template`
  - Filters:
    - `name` eq `path.name`
  - Notes:
    - Response body references #/components/schemas/gitignore-template
    - Query parameters: name
