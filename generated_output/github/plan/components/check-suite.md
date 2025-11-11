# Component Plan: `check-suite`

**API Slug:** `github`
**Total Routes:** 3

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (2)

#### `GET /repos/{owner}/{repo}/check-suites/{check_suite_id}`
**Summary:** Get a check suite
**Status:** planned

**Operations:**
- **read_one**
  - Component: `check-suite`
  - Filters:
    - `owner` eq `path.owner`
    - `repository` eq `path.repo`
    - `check_suite_id` eq `path.check_suite_id`
  - Notes:
    - Response body references #/components/schemas/check-suite

#### `GET /repos/{owner}/{repo}/commits/{ref}/check-suites`
**Summary:** List check suites for a Git reference
**Status:** planned

**Operations:**
- **read_one**
  - Component: `check-suite`
  - Filters:
    - `owner` eq `path.owner`
    - `repository` eq `path.repo`
    - `ref` eq `path.ref`
  - Notes:
    - Query parameters: app_id

### POST Routes (1)

#### `POST /repos/{owner}/{repo}/check-suites`
**Summary:** Create a check suite
**Status:** planned

**Operations:**
- **create**
  - Component: `check-suite`
  - Filters:
    - `owner` eq `path.owner`
    - `repository` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/check-suite
