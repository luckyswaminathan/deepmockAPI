# Component Plan: `license-content`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/license`
**Summary:** Get the license for a repository
**Status:** planned

**Operations:**
- **read_one**
  - Component: `license-content`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/license-content
