# Component Plan: `code-scanning-analysis`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/code-scanning/analyses/{analysis_id}`
**Summary:** Get a code scanning analysis for a repository
**Status:** planned

**Operations:**
- **read_one**
  - Component: `code-scanning-analysis`
  - Filters:
    - `analysis_id` eq `path.analysis_id`
  - Notes:
    - Response body references #/components/schemas/code-scanning-analysis
    - Query parameters: analysis_id
