# Component Plan: `issuing.token`

**API Slug:** `stripe`
**Total Routes:** 2

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /v1/issuing/tokens/{token}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `issuing.token`
  - Filters:
    - `token` eq `path.token`
  - Notes:
    - Response body references #/components/schemas/issuing.token
    - Query parameters: expand

### POST Routes (1)

#### `POST /v1/issuing/tokens/{token}`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.token`
  - Filters:
    - `token` eq `path.token`
  - Notes:
    - Response body references #/components/schemas/issuing.token
    - Query parameters: token
