# Component Plan: `treasury.received_debit`

**API Slug:** `stripe`
**Total Routes:** 2

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /v1/treasury/received_debits/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `treasury.received_debit`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/treasury.received_debit
    - Query parameters: expand

### POST Routes (1)

#### `POST /v1/test_helpers/treasury/received_debits`
**Status:** planned

**Operations:**
- **create**
  - Component: `treasury.received_debit`
  - Notes:
    - Response body references #/components/schemas/treasury.received_debit
