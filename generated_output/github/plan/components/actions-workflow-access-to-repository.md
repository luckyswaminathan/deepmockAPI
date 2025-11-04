# Component Plan: `actions-workflow-access-to-repository`

**API Slug:** `github`
**Total Routes:** 2

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.
- **`update`**: Replace a full record.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/actions/permissions/access`
**Summary:** Get the level of access for workflows outside of the repository
**Status:** planned

**Operations:**
- **read_one**
  - Component: `actions-workflow-access-to-repository`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/actions-workflow-access-to-repository

### PUT Routes (1)

#### `PUT /repos/{owner}/{repo}/actions/permissions/access`
**Summary:** Set the level of access for workflows outside of the repository
**Status:** planned

**Operations:**
- **update**
  - Component: `actions-workflow-access-to-repository`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Request body references #/components/schemas/actions-workflow-access-to-repository
