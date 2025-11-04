# Component Plan: `authorization`

**API Slug:** `github`
**Total Routes:** 3

## Supported Operations
- **`create`**: Create a new record for the component.
- **`update_partial`**: Apply a partial update to a record.

## Routes

### PATCH Routes (1)

#### `PATCH /applications/{client_id}/token`
**Summary:** Reset a token
**Status:** planned

**Operations:**
- **update_partial**
  - Component: `authorization`
  - Filters:
    - `client_id` eq `path.client_id`
  - Notes:
    - Response body references #/components/schemas/authorization

### POST Routes (2)

#### `POST /applications/{client_id}/token`
**Summary:** Check a token
**Status:** planned

**Operations:**
- **create**
  - Component: `authorization`
  - Filters:
    - `client_id` eq `path.client_id`
  - Notes:
    - Response body references #/components/schemas/authorization

#### `POST /applications/{client_id}/token/scoped`
**Summary:** Create a scoped access token
**Status:** planned

**Operations:**
- **create**
  - Component: `authorization`
  - Filters:
    - `client_id` eq `path.client_id`
  - Notes:
    - Response body references #/components/schemas/authorization
