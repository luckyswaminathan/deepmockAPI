# Component Plan: `source`

**API Slug:** `stripe`
**Total Routes:** 7

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (1)

#### `DELETE /v1/customers/{customer}/sources/{id}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `source`
  - Filters:
    - `customer` eq `path.customer`
    - `id` eq `path.id`
  - Notes:
    - Query parameters: customer, id

### GET Routes (2)

#### `GET /v1/customers/{customer}/sources`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `source`
  - Filters:
    - `customer` eq `path.customer`
  - Notes:
    - Query parameters: ending_before, expand, limit, object, starting_after

#### `GET /v1/sources/{source}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `source`
  - Filters:
    - `source_order` eq `path.source`
  - Notes:
    - Response body references #/components/schemas/source
    - Query parameters: client_secret, expand

### POST Routes (4)

#### `POST /v1/customers/{customer}/sources/{id}`
**Status:** planned

**Operations:**
- **create**
  - Component: `source`
  - Filters:
    - `customer` eq `path.customer`
    - `id` eq `path.id`
  - Notes:
    - Query parameters: customer, id

#### `POST /v1/sources`
**Status:** planned

**Operations:**
- **create**
  - Component: `source`
  - Notes:
    - Response body references #/components/schemas/source

#### `POST /v1/sources/{source}`
**Status:** planned

**Operations:**
- **create**
  - Component: `source`
  - Filters:
    - `source_order` eq `path.source`
  - Notes:
    - Response body references #/components/schemas/source
    - Query parameters: source

#### `POST /v1/sources/{source}/verify`
**Status:** planned

**Operations:**
- **create**
  - Component: `source`
  - Filters:
    - `source_order` eq `path.source`
  - Notes:
    - Response body references #/components/schemas/source
    - Query parameters: source
