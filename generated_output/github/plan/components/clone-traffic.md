# Component Plan: `clone-traffic`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/traffic/clones`
**Summary:** Get repository clones
**Status:** planned

**Operations:**
- **read_one**
  - Component: `clone-traffic`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/clone-traffic
