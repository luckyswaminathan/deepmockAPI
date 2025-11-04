# Component Plan: `identity.verification_session`

**API Slug:** `stripe`
**Total Routes:** 5

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /v1/identity/verification_sessions/{session}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `identity.verification_session`
  - Filters:
    - `session` eq `path.session`
  - Notes:
    - Response body references #/components/schemas/identity.verification_session
    - Query parameters: expand

### POST Routes (4)

#### `POST /v1/identity/verification_sessions`
**Status:** planned

**Operations:**
- **create**
  - Component: `identity.verification_session`
  - Notes:
    - Response body references #/components/schemas/identity.verification_session

#### `POST /v1/identity/verification_sessions/{session}`
**Status:** planned

**Operations:**
- **create**
  - Component: `identity.verification_session`
  - Filters:
    - `session` eq `path.session`
  - Notes:
    - Response body references #/components/schemas/identity.verification_session
    - Query parameters: session

#### `POST /v1/identity/verification_sessions/{session}/cancel`
**Status:** planned

**Operations:**
- **create**
  - Component: `identity.verification_session`
  - Filters:
    - `session` eq `path.session`
  - Notes:
    - Response body references #/components/schemas/identity.verification_session
    - Query parameters: session

#### `POST /v1/identity/verification_sessions/{session}/redact`
**Status:** planned

**Operations:**
- **create**
  - Component: `identity.verification_session`
  - Filters:
    - `session` eq `path.session`
  - Notes:
    - Response body references #/components/schemas/identity.verification_session
    - Query parameters: session
