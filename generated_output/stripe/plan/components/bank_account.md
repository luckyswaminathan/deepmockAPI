# Component Plan: `bank_account`

**API Slug:** `stripe`
**Total Routes:** 7

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (2)

#### `DELETE /v1/accounts/{account}/bank_accounts/{id}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `bank_account`
  - Filters:
    - `account` eq `path.account`
    - `id` eq `path.id`
  - Notes:
    - Query parameters: account, id

#### `DELETE /v1/customers/{customer}/bank_accounts/{id}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `bank_account`
  - Filters:
    - `customer` eq `path.customer`
    - `id` eq `path.id`
  - Notes:
    - Query parameters: customer, id

### GET Routes (2)

#### `GET /v1/customers/{customer}/bank_accounts`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `bank_account`
  - Filters:
    - `customer` eq `path.customer`
  - Notes:
    - Query parameters: ending_before, expand, limit, starting_after

#### `GET /v1/customers/{customer}/bank_accounts/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `bank_account`
  - Filters:
    - `customer` eq `path.customer`
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/bank_account
    - Query parameters: expand

### POST Routes (3)

#### `POST /v1/customers/{customer}/bank_accounts/{id}`
**Status:** planned

**Operations:**
- **create**
  - Component: `bank_account`
  - Filters:
    - `customer` eq `path.customer`
    - `id` eq `path.id`
  - Notes:
    - Query parameters: customer, id

#### `POST /v1/customers/{customer}/bank_accounts/{id}/verify`
**Status:** planned

**Operations:**
- **create**
  - Component: `bank_account`
  - Filters:
    - `customer` eq `path.customer`
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/bank_account
    - Query parameters: customer, id

#### `POST /v1/customers/{customer}/sources/{id}/verify`
**Status:** planned

**Operations:**
- **create**
  - Component: `bank_account`
  - Filters:
    - `customer` eq `path.customer`
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/bank_account
    - Query parameters: customer, id
