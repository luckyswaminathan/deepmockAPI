# Component Plan: `code-scanning-sarifs-receipt`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`create`**: Create a new record for the component.

## Routes

### POST Routes (1)

#### `POST /repos/{owner}/{repo}/code-scanning/sarifs`
**Summary:** Upload an analysis as SARIF data
**Status:** planned

**Operations:**
- **create**
  - Component: `code-scanning-sarifs-receipt`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/code-scanning-sarifs-receipt
