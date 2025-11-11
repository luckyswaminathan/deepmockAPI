# Component Plan: `participation-stats`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/stats/participation`
**Summary:** Get the weekly commit count
**Status:** planned

**Operations:**
- **read_one**
  - Component: `participation-stats`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/participation-stats
