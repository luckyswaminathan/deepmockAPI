# Component Plan: `token`

**API Slug:** `stripe`
**Total Routes:** 3

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.

## Routes

### GET Routes (2)

#### `GET /v1/issuing/tokens`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `token`
  - Notes:
    - Query parameters: card, created, ending_before, expand, limit, starting_after, status

#### `GET /v1/tokens/{token}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `token`
  - Filters:
    - `token` eq `path.token`
  - Notes:
    - Response body references #/components/schemas/token
    - Query parameters: expand

### POST Routes (1)

#### `POST /v1/tokens`
**Status:** planned

**Operations:**
- **create**
  - Component: `token`
  - Notes:
    - Response body references #/components/schemas/token
