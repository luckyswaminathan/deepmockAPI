# Component Plan: `content-tree`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/contents/{path}`
**Summary:** Get repository content
**Status:** planned

**Operations:**
- **read_one**
  - Component: `content-tree`
  - Filters:
    - `path` eq `path.path`
  - Notes:
    - Response body references #/components/schemas/content-tree
    - Query parameters: ref
