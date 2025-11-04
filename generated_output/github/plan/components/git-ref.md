# Component Plan: `git-ref`

**API Slug:** `github`
**Total Routes:** 3

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`update_partial`**: Apply a partial update to a record.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/git/ref/{ref}`
**Summary:** Get a reference
**Status:** planned

**Operations:**
- **read_one**
  - Component: `git-ref`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `ref` eq `path.ref`
  - Notes:
    - Response body references #/components/schemas/git-ref

### PATCH Routes (1)

#### `PATCH /repos/{owner}/{repo}/git/refs/{ref}`
**Summary:** Update a reference
**Status:** planned

**Operations:**
- **update_partial**
  - Component: `git-ref`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `ref` eq `path.ref`
  - Notes:
    - Response body references #/components/schemas/git-ref

### POST Routes (1)

#### `POST /repos/{owner}/{repo}/git/refs`
**Summary:** Create a reference
**Status:** planned

**Operations:**
- **create**
  - Component: `git-ref`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/git-ref
