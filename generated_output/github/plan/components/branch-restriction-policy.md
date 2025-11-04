# Component Plan: `branch-restriction-policy`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/branches/{branch}/protection/restrictions`
**Summary:** Get access restrictions
**Status:** planned

**Operations:**
- **read_one**
  - Component: `branch-restriction-policy`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `branch` eq `path.branch`
  - Notes:
    - Response body references #/components/schemas/branch-restriction-policy
