# Component Plan: `check-run`

**API Slug:** `github`
**Total Routes:** 5

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`update_partial`**: Apply a partial update to a record.

## Routes

### GET Routes (3)

#### `GET /repos/{owner}/{repo}/check-runs/{check_run_id}`
**Summary:** Get a check run
**Status:** planned

**Operations:**
- **read_one**
  - Component: `check-run`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `check_run_id` eq `path.check_run_id`
  - Notes:
    - Response body references #/components/schemas/check-run

#### `GET /repos/{owner}/{repo}/check-suites/{check_suite_id}/check-runs`
**Summary:** List check runs in a check suite
**Status:** planned

**Operations:**
- **read_one**
  - Component: `check-run`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `check_suite_id` eq `path.check_suite_id`
  - Notes:
    - Query parameters: filter

#### `GET /repos/{owner}/{repo}/commits/{ref}/check-runs`
**Summary:** List check runs for a Git reference
**Status:** planned

**Operations:**
- **read_one**
  - Component: `check-run`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `ref` eq `path.ref`
  - Notes:
    - Query parameters: filter, app_id

### PATCH Routes (1)

#### `PATCH /repos/{owner}/{repo}/check-runs/{check_run_id}`
**Summary:** Update a check run
**Status:** planned

**Operations:**
- **update_partial**
  - Component: `check-run`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `check_run_id` eq `path.check_run_id`
  - Notes:
    - Response body references #/components/schemas/check-run

### POST Routes (1)

#### `POST /repos/{owner}/{repo}/check-runs`
**Summary:** Create a check run
**Status:** planned

**Operations:**
- **create**
  - Component: `check-run`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/check-run
