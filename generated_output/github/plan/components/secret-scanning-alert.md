# Component Plan: `secret-scanning-alert`

**API Slug:** `github`
**Total Routes:** 2

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.
- **`update_partial`**: Apply a partial update to a record.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/secret-scanning/alerts/{alert_number}`
**Summary:** Get a secret scanning alert
**Status:** planned

**Operations:**
- **read_one**
  - Component: `secret-scanning-alert`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `alert_number` eq `path.alert_number`
  - Notes:
    - Response body references #/components/schemas/secret-scanning-alert

### PATCH Routes (1)

#### `PATCH /repos/{owner}/{repo}/secret-scanning/alerts/{alert_number}`
**Summary:** Update a secret scanning alert
**Status:** planned

**Operations:**
- **update_partial**
  - Component: `secret-scanning-alert`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `alert_number` eq `path.alert_number`
  - Notes:
    - Response body references #/components/schemas/secret-scanning-alert
