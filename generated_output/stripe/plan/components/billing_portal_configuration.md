# Component Plan: `billing_portal.configuration`

**API Slug:** `stripe`
**Total Routes:** 3

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /v1/billing_portal/configurations/{configuration}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `billing_portal.configuration`
  - Filters:
    - `configuration` eq `path.configuration`
  - Notes:
    - Response body references #/components/schemas/billing_portal.configuration
    - Query parameters: expand

### POST Routes (2)

#### `POST /v1/billing_portal/configurations`
**Status:** planned

**Operations:**
- **create**
  - Component: `billing_portal.configuration`
  - Notes:
    - Response body references #/components/schemas/billing_portal.configuration

#### `POST /v1/billing_portal/configurations/{configuration}`
**Status:** planned

**Operations:**
- **create**
  - Component: `billing_portal.configuration`
  - Filters:
    - `configuration` eq `path.configuration`
  - Notes:
    - Response body references #/components/schemas/billing_portal.configuration
    - Query parameters: configuration
