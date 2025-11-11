# Component Plan: `status-check-policy`

**API Slug:** `github`
**Total Routes:** 2

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.
- **`update_partial`**: Apply a partial update to a record.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/branches/{branch}/protection/required_status_checks`
**Summary:** Get status checks protection
**Status:** planned

**Operations:**
- **read_one**
  - Component: `status-check-policy`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `branch` eq `path.branch`
  - Notes:
    - Response body references #/components/schemas/status-check-policy

### PATCH Routes (1)

#### `PATCH /repos/{owner}/{repo}/branches/{branch}/protection/required_status_checks`
**Summary:** Update status check protection
**Status:** planned

**Operations:**
- **update_partial**
  - Component: `status-check-policy`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `branch` eq `path.branch`
  - Notes:
    - Response body references #/components/schemas/status-check-policy
