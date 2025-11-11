# Component Plan: `code-scanning-alert`

**API Slug:** `github`
**Total Routes:** 2

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.
- **`update_partial`**: Apply a partial update to a record.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/code-scanning/alerts/{alert_number}`
**Summary:** Get a code scanning alert
**Status:** planned

**Operations:**
- **read_one**
  - Component: `code-scanning-alert`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `alert_number` eq `path.alert_number`
  - Notes:
    - Response body references #/components/schemas/code-scanning-alert

### PATCH Routes (1)

#### `PATCH /repos/{owner}/{repo}/code-scanning/alerts/{alert_number}`
**Summary:** Update a code scanning alert
**Status:** planned

**Operations:**
- **update_partial**
  - Component: `code-scanning-alert`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `alert_number` eq `path.alert_number`
  - Notes:
    - Response body references #/components/schemas/code-scanning-alert
