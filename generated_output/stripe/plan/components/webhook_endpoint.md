# Component Plan: `webhook_endpoint`

**API Slug:** `stripe`
**Total Routes:** 5

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (1)

#### `DELETE /v1/webhook_endpoints/{webhook_endpoint}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `webhook_endpoint`
  - Filters:
    - `webhook_endpoint` eq `path.webhook_endpoint`
  - Notes:
    - Query parameters: webhook_endpoint

### GET Routes (2)

#### `GET /v1/webhook_endpoints`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `webhook_endpoint`
  - Notes:
    - Query parameters: ending_before, expand, limit, starting_after

#### `GET /v1/webhook_endpoints/{webhook_endpoint}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `webhook_endpoint`
  - Filters:
    - `webhook_endpoint` eq `path.webhook_endpoint`
  - Notes:
    - Response body references #/components/schemas/webhook_endpoint
    - Query parameters: expand

### POST Routes (2)

#### `POST /v1/webhook_endpoints`
**Status:** planned

**Operations:**
- **create**
  - Component: `webhook_endpoint`
  - Notes:
    - Response body references #/components/schemas/webhook_endpoint

#### `POST /v1/webhook_endpoints/{webhook_endpoint}`
**Status:** planned

**Operations:**
- **create**
  - Component: `webhook_endpoint`
  - Filters:
    - `webhook_endpoint` eq `path.webhook_endpoint`
  - Notes:
    - Response body references #/components/schemas/webhook_endpoint
    - Query parameters: webhook_endpoint
