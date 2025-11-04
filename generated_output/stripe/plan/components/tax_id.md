# Component Plan: `tax_id`

**API Slug:** `stripe`
**Total Routes:** 8

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (2)

#### `DELETE /v1/customers/{customer}/tax_ids/{id}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `tax_id`
  - Filters:
    - `customer` eq `path.customer`
    - `id` eq `path.id`
  - Notes:
    - Query parameters: customer, id

#### `DELETE /v1/tax_ids/{id}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `tax_id`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Query parameters: id

### GET Routes (4)

#### `GET /v1/customers/{customer}/tax_ids`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `tax_id`
  - Filters:
    - `customer` eq `path.customer`
  - Notes:
    - Query parameters: ending_before, expand, limit, starting_after

#### `GET /v1/customers/{customer}/tax_ids/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `tax_id`
  - Filters:
    - `customer` eq `path.customer`
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/tax_id
    - Query parameters: expand

#### `GET /v1/tax_ids`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `tax_id`
  - Notes:
    - Query parameters: ending_before, expand, limit, owner, starting_after

#### `GET /v1/tax_ids/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `tax_id`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/tax_id
    - Query parameters: expand

### POST Routes (2)

#### `POST /v1/customers/{customer}/tax_ids`
**Status:** planned

**Operations:**
- **create**
  - Component: `tax_id`
  - Filters:
    - `customer` eq `path.customer`
  - Notes:
    - Response body references #/components/schemas/tax_id
    - Query parameters: customer

#### `POST /v1/tax_ids`
**Status:** planned

**Operations:**
- **create**
  - Component: `tax_id`
  - Notes:
    - Response body references #/components/schemas/tax_id
