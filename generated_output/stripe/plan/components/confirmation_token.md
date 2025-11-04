# Component Plan: `confirmation_token`

**API Slug:** `stripe`
**Total Routes:** 2

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /v1/confirmation_tokens/{confirmation_token}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `confirmation_token`
  - Filters:
    - `confirmation_token` eq `path.confirmation_token`
  - Notes:
    - Response body references #/components/schemas/confirmation_token
    - Query parameters: expand

### POST Routes (1)

#### `POST /v1/test_helpers/confirmation_tokens`
**Status:** planned

**Operations:**
- **create**
  - Component: `confirmation_token`
  - Notes:
    - Response body references #/components/schemas/confirmation_token
