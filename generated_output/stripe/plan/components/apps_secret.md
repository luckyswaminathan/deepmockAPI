# Component Plan: `apps.secret`

**API Slug:** `stripe`
**Total Routes:** 3

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_many`**: List or search records.

## Routes

### GET Routes (1)

#### `GET /v1/apps/secrets/find`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `apps.secret`
  - Notes:
    - Response body references #/components/schemas/apps.secret
    - Query parameters: expand, name, scope

### POST Routes (2)

#### `POST /v1/apps/secrets`
**Status:** planned

**Operations:**
- **create**
  - Component: `apps.secret`
  - Notes:
    - Response body references #/components/schemas/apps.secret

#### `POST /v1/apps/secrets/delete`
**Status:** planned

**Operations:**
- **create**
  - Component: `apps.secret`
  - Notes:
    - Response body references #/components/schemas/apps.secret
