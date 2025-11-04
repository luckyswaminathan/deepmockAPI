# Component Plan: `payment_source`

**API Slug:** `stripe`
**Total Routes:** 4

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /v1/customers/{customer}/sources/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `payment_source`
  - Filters:
    - `customer` eq `path.customer`
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/payment_source
    - Query parameters: expand

### POST Routes (3)

#### `POST /v1/customers/{customer}/bank_accounts`
**Status:** planned

**Operations:**
- **create**
  - Component: `payment_source`
  - Filters:
    - `customer` eq `path.customer`
  - Notes:
    - Response body references #/components/schemas/payment_source
    - Query parameters: customer

#### `POST /v1/customers/{customer}/cards`
**Status:** planned

**Operations:**
- **create**
  - Component: `payment_source`
  - Filters:
    - `customer` eq `path.customer`
  - Notes:
    - Response body references #/components/schemas/payment_source
    - Query parameters: customer

#### `POST /v1/customers/{customer}/sources`
**Status:** planned

**Operations:**
- **create**
  - Component: `payment_source`
  - Filters:
    - `customer` eq `path.customer`
  - Notes:
    - Response body references #/components/schemas/payment_source
    - Query parameters: customer
