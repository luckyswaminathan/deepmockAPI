# Component Plan: `combined-commit-status`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/commits/{ref}/status`
**Summary:** Get the combined status for a specific reference
**Status:** planned

**Operations:**
- **read_one**
  - Component: `combined-commit-status`
  - Filters:
    - `owner` eq `path.owner`
    - `repository` eq `path.repo`
    - `ref` eq `path.ref`
  - Notes:
    - Response body references #/components/schemas/combined-commit-status
