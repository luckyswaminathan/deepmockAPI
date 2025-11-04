# Component Plan: `branch-protection`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/branches/{branch}/protection`
**Summary:** Get branch protection
**Status:** planned

**Operations:**
- **read_one**
  - Component: `branch-protection`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `lock_branch` eq `path.branch`
  - Notes:
    - Response body references #/components/schemas/branch-protection
