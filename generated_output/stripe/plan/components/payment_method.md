# Component Plan: `payment_method`

**API Slug:** `stripe`
**Total Routes:** 8

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.

## Routes

### GET Routes (4)

#### `GET /v1/customers/{customer}/payment_methods`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `payment_method`
  - Filters:
    - `customer` eq `path.customer`
  - Notes:
    - Query parameters: allow_redisplay, ending_before, expand, limit, starting_after, type

#### `GET /v1/customers/{customer}/payment_methods/{payment_method}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `payment_method`
  - Filters:
    - `customer` eq `path.customer`
    - `payment_method` eq `path.payment_method`
  - Notes:
    - Response body references #/components/schemas/payment_method
    - Query parameters: expand

#### `GET /v1/payment_methods`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `payment_method`
  - Notes:
    - Query parameters: customer, ending_before, expand, limit, starting_after, type

#### `GET /v1/payment_methods/{payment_method}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `payment_method`
  - Filters:
    - `payment_method` eq `path.payment_method`
  - Notes:
    - Response body references #/components/schemas/payment_method
    - Query parameters: expand

### POST Routes (4)

#### `POST /v1/payment_methods`
**Status:** planned

**Operations:**
- **create**
  - Component: `payment_method`
  - Notes:
    - Response body references #/components/schemas/payment_method

#### `POST /v1/payment_methods/{payment_method}`
**Status:** planned

**Operations:**
- **create**
  - Component: `payment_method`
  - Filters:
    - `payment_method` eq `path.payment_method`
  - Notes:
    - Response body references #/components/schemas/payment_method
    - Query parameters: payment_method

#### `POST /v1/payment_methods/{payment_method}/attach`
**Status:** planned

**Operations:**
- **create**
  - Component: `payment_method`
  - Filters:
    - `payment_method` eq `path.payment_method`
  - Notes:
    - Response body references #/components/schemas/payment_method
    - Query parameters: payment_method

#### `POST /v1/payment_methods/{payment_method}/detach`
**Status:** planned

**Operations:**
- **create**
  - Component: `payment_method`
  - Filters:
    - `payment_method` eq `path.payment_method`
  - Notes:
    - Response body references #/components/schemas/payment_method
    - Query parameters: payment_method
