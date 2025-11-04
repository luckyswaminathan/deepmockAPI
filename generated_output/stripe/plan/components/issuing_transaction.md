# Component Plan: `issuing.transaction`

**API Slug:** `stripe`
**Total Routes:** 5

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /v1/issuing/transactions/{transaction}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `issuing.transaction`
  - Filters:
    - `balance_transaction` eq `path.transaction`
  - Notes:
    - Response body references #/components/schemas/issuing.transaction
    - Query parameters: expand

### POST Routes (4)

#### `POST /v1/issuing/transactions/{transaction}`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.transaction`
  - Filters:
    - `balance_transaction` eq `path.transaction`
  - Notes:
    - Response body references #/components/schemas/issuing.transaction
    - Query parameters: transaction

#### `POST /v1/test_helpers/issuing/transactions/create_force_capture`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.transaction`
  - Notes:
    - Response body references #/components/schemas/issuing.transaction

#### `POST /v1/test_helpers/issuing/transactions/create_unlinked_refund`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.transaction`
  - Notes:
    - Response body references #/components/schemas/issuing.transaction

#### `POST /v1/test_helpers/issuing/transactions/{transaction}/refund`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.transaction`
  - Filters:
    - `balance_transaction` eq `path.transaction`
  - Notes:
    - Response body references #/components/schemas/issuing.transaction
    - Query parameters: transaction
