# Component Plan: `milestone`

**API Slug:** `github`
**Total Routes:** 5

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`update_partial`**: Apply a partial update to a record.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (1)

#### `DELETE /repos/{owner}/{repo}/milestones/{milestone_number}`
**Summary:** Delete a milestone
**Status:** planned

**Operations:**
- **delete**
  - Component: `milestone`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `milestone_number` eq `path.milestone_number`

### GET Routes (2)

#### `GET /repos/{owner}/{repo}/milestones`
**Summary:** List milestones
**Status:** planned

**Operations:**
- **read_one**
  - Component: `milestone`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Query parameters: state, sort, direction

#### `GET /repos/{owner}/{repo}/milestones/{milestone_number}`
**Summary:** Get a milestone
**Status:** planned

**Operations:**
- **read_one**
  - Component: `milestone`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `milestone_number` eq `path.milestone_number`
  - Notes:
    - Response body references #/components/schemas/milestone

### PATCH Routes (1)

#### `PATCH /repos/{owner}/{repo}/milestones/{milestone_number}`
**Summary:** Update a milestone
**Status:** planned

**Operations:**
- **update_partial**
  - Component: `milestone`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `milestone_number` eq `path.milestone_number`
  - Notes:
    - Response body references #/components/schemas/milestone

### POST Routes (1)

#### `POST /repos/{owner}/{repo}/milestones`
**Summary:** Create a milestone
**Status:** planned

**Operations:**
- **create**
  - Component: `milestone`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/milestone
