# Component Plan: `tax.transaction`

**API Slug:** `stripe`
**Total Routes:** 3

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /v1/tax/transactions/{transaction}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `tax.transaction`
  - Filters:
    - `transaction` eq `path.transaction`
  - Notes:
    - Response body references #/components/schemas/tax.transaction
    - Query parameters: expand

### POST Routes (2)

#### `POST /v1/tax/transactions/create_from_calculation`
**Status:** planned

**Operations:**
- **create**
  - Component: `tax.transaction`
  - Notes:
    - Response body references #/components/schemas/tax.transaction

#### `POST /v1/tax/transactions/create_reversal`
**Status:** planned

**Operations:**
- **create**
  - Component: `tax.transaction`
  - Notes:
    - Response body references #/components/schemas/tax.transaction
