# Component Plan: `codespaces-permissions-check-for-devcontainer`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/codespaces/permissions_check`
**Summary:** Check if permissions defined by a devcontainer have been accepted by the authenticated user
**Status:** planned

**Operations:**
- **read_one**
  - Component: `codespaces-permissions-check-for-devcontainer`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/codespaces-permissions-check-for-devcontainer
    - Query parameters: ref, devcontainer_path
