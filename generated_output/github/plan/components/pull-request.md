# Component Plan: `pull-request`

**API Slug:** `github`
**Total Routes:** 3

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`update_partial`**: Apply a partial update to a record.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/pulls/{pull_number}`
**Summary:** Get a pull request
**Status:** planned

**Operations:**
- **read_one**
  - Component: `pull-request`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `pull_number` eq `path.pull_number`
  - Notes:
    - Response body references #/components/schemas/pull-request

### PATCH Routes (1)

#### `PATCH /repos/{owner}/{repo}/pulls/{pull_number}`
**Summary:** Update a pull request
**Status:** planned

**Operations:**
- **update_partial**
  - Component: `pull-request`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `pull_number` eq `path.pull_number`
  - Notes:
    - Response body references #/components/schemas/pull-request

### POST Routes (1)

#### `POST /repos/{owner}/{repo}/pulls`
**Summary:** Create a pull request
**Status:** planned

**Operations:**
- **create**
  - Component: `pull-request`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/pull-request
