# Component Plan: `card`

**API Slug:** `stripe`
**Total Routes:** 5

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (1)

#### `DELETE /v1/customers/{customer}/cards/{id}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `card`
  - Filters:
    - `customer` eq `path.customer`
    - `id` eq `path.id`
  - Notes:
    - Query parameters: customer, id

### GET Routes (3)

#### `GET /v1/customers/{customer}/cards`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `card`
  - Filters:
    - `customer` eq `path.customer`
  - Notes:
    - Query parameters: ending_before, expand, limit, starting_after

#### `GET /v1/customers/{customer}/cards/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `card`
  - Filters:
    - `customer` eq `path.customer`
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/card
    - Query parameters: expand

#### `GET /v1/issuing/cards`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `card`
  - Notes:
    - Query parameters: cardholder, created, ending_before, exp_month, exp_year, expand, last4, limit, personalization_design, starting_after, status, type

### POST Routes (1)

#### `POST /v1/customers/{customer}/cards/{id}`
**Status:** planned

**Operations:**
- **create**
  - Component: `card`
  - Filters:
    - `customer` eq `path.customer`
    - `id` eq `path.id`
  - Notes:
    - Query parameters: customer, id
