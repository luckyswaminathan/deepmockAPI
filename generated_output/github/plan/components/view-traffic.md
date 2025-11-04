# Component Plan: `view-traffic`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/traffic/views`
**Summary:** Get page views
**Status:** planned

**Operations:**
- **read_one**
  - Component: `view-traffic`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/view-traffic
