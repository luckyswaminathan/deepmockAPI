# Component Plan: `product`

**API Slug:** `stripe`
**Total Routes:** 6

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (1)

#### `DELETE /v1/products/{id}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `product`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Query parameters: id

### GET Routes (3)

#### `GET /v1/climate/products`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `product`
  - Notes:
    - Query parameters: ending_before, expand, limit, starting_after

#### `GET /v1/products`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `product`
  - Notes:
    - Query parameters: active, created, ending_before, expand, ids, limit, shippable, starting_after, url

#### `GET /v1/products/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `product`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/product
    - Query parameters: expand

### POST Routes (2)

#### `POST /v1/products`
**Status:** planned

**Operations:**
- **create**
  - Component: `product`
  - Notes:
    - Response body references #/components/schemas/product

#### `POST /v1/products/{id}`
**Status:** planned

**Operations:**
- **create**
  - Component: `product`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/product
    - Query parameters: id
