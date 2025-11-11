# Component Plan: `actions-repository-permissions`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/actions/permissions`
**Summary:** Get GitHub Actions permissions for a repository
**Status:** planned

**Operations:**
- **read_one**
  - Component: `actions-repository-permissions`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/actions-repository-permissions
