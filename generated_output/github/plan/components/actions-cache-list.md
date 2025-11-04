# Component Plan: `actions-cache-list`

**API Slug:** `github`
**Total Routes:** 2

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (1)

#### `DELETE /repos/{owner}/{repo}/actions/caches`
**Summary:** Delete GitHub Actions caches for a repository (using a cache key)
**Status:** planned

**Operations:**
- **delete**
  - Component: `actions-cache-list`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/actions-cache-list

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/actions/caches`
**Summary:** List GitHub Actions caches for a repository
**Status:** planned

**Operations:**
- **read_one**
  - Component: `actions-cache-list`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/actions-cache-list
