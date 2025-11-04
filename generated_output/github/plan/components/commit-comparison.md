# Component Plan: `commit-comparison`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/compare/{basehead}`
**Summary:** Compare two commits
**Status:** planned

**Operations:**
- **read_one**
  - Component: `commit-comparison`
  - Filters:
    - `basehead` eq `path.basehead`
  - Notes:
    - Response body references #/components/schemas/commit-comparison
    - Query parameters: basehead
