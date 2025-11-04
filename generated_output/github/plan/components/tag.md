# Component Plan: `tag`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/tags`
**Summary:** List repository tags
**Status:** planned

**Operations:**
- **read_one**
  - Component: `tag`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
