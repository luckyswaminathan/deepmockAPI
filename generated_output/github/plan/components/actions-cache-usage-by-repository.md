# Component Plan: `actions-cache-usage-by-repository`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/actions/cache/usage`
**Summary:** Get GitHub Actions cache usage for a repository
**Status:** planned

**Operations:**
- **read_one**
  - Component: `actions-cache-usage-by-repository`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/actions-cache-usage-by-repository
