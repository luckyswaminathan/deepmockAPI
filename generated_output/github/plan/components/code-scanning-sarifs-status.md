# Component Plan: `code-scanning-sarifs-status`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/code-scanning/sarifs/{sarif_id}`
**Summary:** Get information about a SARIF upload
**Status:** planned

**Operations:**
- **read_one**
  - Component: `code-scanning-sarifs-status`
  - Filters:
    - `sarif_id` eq `path.sarif_id`
  - Notes:
    - Response body references #/components/schemas/code-scanning-sarifs-status
    - Query parameters: sarif_id
