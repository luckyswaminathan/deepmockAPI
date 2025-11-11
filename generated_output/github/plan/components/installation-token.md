# Component Plan: `installation-token`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`create`**: Create a new record for the component.

## Routes

### POST Routes (1)

#### `POST /app/installations/{installation_id}/access_tokens`
**Summary:** Create an installation access token for an app
**Status:** planned

**Operations:**
- **create**
  - Component: `installation-token`
  - Filters:
    - `installation_id` eq `path.installation_id`
  - Notes:
    - Response body references #/components/schemas/installation-token
