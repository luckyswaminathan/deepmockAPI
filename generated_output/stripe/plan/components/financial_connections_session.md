# Component Plan: `financial_connections.session`

**API Slug:** `stripe`
**Total Routes:** 4

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (2)

#### `GET /v1/financial_connections/sessions/{session}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `financial_connections.session`
  - Filters:
    - `session` eq `path.session`
  - Notes:
    - Response body references #/components/schemas/financial_connections.session
    - Query parameters: expand

#### `GET /v1/link_account_sessions/{session}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `financial_connections.session`
  - Filters:
    - `session` eq `path.session`
  - Notes:
    - Response body references #/components/schemas/financial_connections.session
    - Query parameters: expand

### POST Routes (2)

#### `POST /v1/financial_connections/sessions`
**Status:** planned

**Operations:**
- **create**
  - Component: `financial_connections.session`
  - Notes:
    - Response body references #/components/schemas/financial_connections.session

#### `POST /v1/link_account_sessions`
**Status:** planned

**Operations:**
- **create**
  - Component: `financial_connections.session`
  - Notes:
    - Response body references #/components/schemas/financial_connections.session
