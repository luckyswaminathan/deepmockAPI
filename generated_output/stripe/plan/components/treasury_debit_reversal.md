# Component Plan: `treasury.debit_reversal`

**API Slug:** `stripe`
**Total Routes:** 2

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /v1/treasury/debit_reversals/{debit_reversal}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `treasury.debit_reversal`
  - Filters:
    - `debit_reversal` eq `path.debit_reversal`
  - Notes:
    - Response body references #/components/schemas/treasury.debit_reversal
    - Query parameters: expand

### POST Routes (1)

#### `POST /v1/treasury/debit_reversals`
**Status:** planned

**Operations:**
- **create**
  - Component: `treasury.debit_reversal`
  - Notes:
    - Response body references #/components/schemas/treasury.debit_reversal
