# Component Plan: `forwarding.request`

**API Slug:** `stripe`
**Total Routes:** 2

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /v1/forwarding/requests/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `forwarding.request`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/forwarding.request
    - Query parameters: expand

### POST Routes (1)

#### `POST /v1/forwarding/requests`
**Status:** planned

**Operations:**
- **create**
  - Component: `forwarding.request`
  - Notes:
    - Response body references #/components/schemas/forwarding.request
