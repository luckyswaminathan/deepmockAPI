# Component Plan: `checkout.session`

**API Slug:** `stripe`
**Total Routes:** 4

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /v1/checkout/sessions/{session}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `checkout.session`
  - Filters:
    - `session` eq `path.session`
  - Notes:
    - Response body references #/components/schemas/checkout.session
    - Query parameters: expand

### POST Routes (3)

#### `POST /v1/checkout/sessions`
**Status:** planned

**Operations:**
- **create**
  - Component: `checkout.session`
  - Notes:
    - Response body references #/components/schemas/checkout.session

#### `POST /v1/checkout/sessions/{session}`
**Status:** planned

**Operations:**
- **create**
  - Component: `checkout.session`
  - Filters:
    - `session` eq `path.session`
  - Notes:
    - Response body references #/components/schemas/checkout.session
    - Query parameters: session

#### `POST /v1/checkout/sessions/{session}/expire`
**Status:** planned

**Operations:**
- **create**
  - Component: `checkout.session`
  - Filters:
    - `session` eq `path.session`
  - Notes:
    - Response body references #/components/schemas/checkout.session
    - Query parameters: session
