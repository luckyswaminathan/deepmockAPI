# Component Plan: `treasury.credit_reversal`

**API Slug:** `stripe`
**Total Routes:** 2

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /v1/treasury/credit_reversals/{credit_reversal}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `treasury.credit_reversal`
  - Filters:
    - `credit_reversal` eq `path.credit_reversal`
  - Notes:
    - Response body references #/components/schemas/treasury.credit_reversal
    - Query parameters: expand

### POST Routes (1)

#### `POST /v1/treasury/credit_reversals`
**Status:** planned

**Operations:**
- **create**
  - Component: `treasury.credit_reversal`
  - Notes:
    - Response body references #/components/schemas/treasury.credit_reversal
