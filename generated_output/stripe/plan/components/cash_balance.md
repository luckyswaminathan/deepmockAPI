# Component Plan: `cash_balance`

**API Slug:** `stripe`
**Total Routes:** 2

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /v1/customers/{customer}/cash_balance`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `cash_balance`
  - Filters:
    - `customer` eq `path.customer`
  - Notes:
    - Response body references #/components/schemas/cash_balance
    - Query parameters: expand

### POST Routes (1)

#### `POST /v1/customers/{customer}/cash_balance`
**Status:** planned

**Operations:**
- **create**
  - Component: `cash_balance`
  - Filters:
    - `customer` eq `path.customer`
  - Notes:
    - Response body references #/components/schemas/cash_balance
    - Query parameters: customer
