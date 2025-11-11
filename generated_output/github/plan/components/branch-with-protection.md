# Component Plan: `branch-with-protection`

**API Slug:** `github`
**Total Routes:** 2

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/branches/{branch}`
**Summary:** Get a branch
**Status:** planned

**Operations:**
- **read_one**
  - Component: `branch-with-protection`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `branch` eq `path.branch`
  - Notes:
    - Response body references #/components/schemas/branch-with-protection

### POST Routes (1)

#### `POST /repos/{owner}/{repo}/branches/{branch}/rename`
**Summary:** Rename a branch
**Status:** planned

**Operations:**
- **create**
  - Component: `branch-with-protection`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `branch` eq `path.branch`
  - Notes:
    - Response body references #/components/schemas/branch-with-protection
