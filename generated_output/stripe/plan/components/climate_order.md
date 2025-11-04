# Component Plan: `climate.order`

**API Slug:** `stripe`
**Total Routes:** 4

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /v1/climate/orders/{order}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `climate.order`
  - Filters:
    - `order` eq `path.order`
  - Notes:
    - Response body references #/components/schemas/climate.order
    - Query parameters: expand

### POST Routes (3)

#### `POST /v1/climate/orders`
**Status:** planned

**Operations:**
- **create**
  - Component: `climate.order`
  - Notes:
    - Response body references #/components/schemas/climate.order

#### `POST /v1/climate/orders/{order}`
**Status:** planned

**Operations:**
- **create**
  - Component: `climate.order`
  - Filters:
    - `order` eq `path.order`
  - Notes:
    - Response body references #/components/schemas/climate.order
    - Query parameters: order

#### `POST /v1/climate/orders/{order}/cancel`
**Status:** planned

**Operations:**
- **create**
  - Component: `climate.order`
  - Filters:
    - `order` eq `path.order`
  - Notes:
    - Response body references #/components/schemas/climate.order
    - Query parameters: order
