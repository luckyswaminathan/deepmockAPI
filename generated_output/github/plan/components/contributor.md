# Component Plan: `contributor`

**API Slug:** `github`
**Total Routes:** 2

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (2)

#### `GET /repos/{owner}/{repo}/contributors`
**Summary:** List repository contributors
**Status:** planned

**Operations:**
- **read_one**
  - Component: `contributor`
  - Filters:
    - `owner` eq `path.owner`
    - `repos_url` eq `path.repo`
  - Notes:
    - Query parameters: anon

#### `GET /repos/{owner}/{repo}/stats/contributors`
**Summary:** Get all contributor commit activity
**Status:** planned

**Operations:**
- **read_one**
  - Component: `contributor`
  - Filters:
    - `owner` eq `path.owner`
    - `repos_url` eq `path.repo`
