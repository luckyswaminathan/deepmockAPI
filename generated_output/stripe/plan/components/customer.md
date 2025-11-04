# Component Plan: `customer`

**API Slug:** `stripe`
**Total Routes:** 5

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (1)

#### `DELETE /v1/customers/{customer}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `customer`
  - Filters:
    - `customer` eq `path.customer`
  - Notes:
    - Query parameters: customer

### GET Routes (2)

#### `GET /v1/customers`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `customer`
  - Notes:
    - Query parameters: created, email, ending_before, expand, limit, starting_after, test_clock

#### `GET /v1/customers/{customer}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `customer`
  - Filters:
    - `customer` eq `path.customer`
  - Notes:
    - Query parameters: expand

### POST Routes (2)

#### `POST /v1/customers`
**Status:** planned

**Operations:**
- **create**
  - Component: `customer`
  - Notes:
    - Response body references #/components/schemas/customer

#### `POST /v1/customers/{customer}`
**Status:** planned

**Operations:**
- **create**
  - Component: `customer`
  - Filters:
    - `customer` eq `path.customer`
  - Notes:
    - Response body references #/components/schemas/customer
    - Query parameters: customer
