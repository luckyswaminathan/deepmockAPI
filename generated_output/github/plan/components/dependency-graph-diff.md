# Component Plan: `dependency-graph-diff`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/dependency-graph/compare/{basehead}`
**Summary:** Get a diff of the dependencies between commits
**Status:** planned

**Operations:**
- **read_one**
  - Component: `dependency-graph-diff`
  - Filters:
    - `basehead` eq `path.basehead`
  - Notes:
    - Response body references #/components/schemas/dependency-graph-diff
    - Query parameters: basehead
