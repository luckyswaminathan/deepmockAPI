# Component Plan: `transfer_reversal`

**API Slug:** `stripe`
**Total Routes:** 3

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /v1/transfers/{transfer}/reversals/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `transfer_reversal`
  - Filters:
    - `id` eq `path.id`
    - `transfer` eq `path.transfer`
  - Notes:
    - Response body references #/components/schemas/transfer_reversal
    - Query parameters: expand

### POST Routes (2)

#### `POST /v1/transfers/{id}/reversals`
**Status:** planned

**Operations:**
- **create**
  - Component: `transfer_reversal`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/transfer_reversal
    - Query parameters: id

#### `POST /v1/transfers/{transfer}/reversals/{id}`
**Status:** planned

**Operations:**
- **create**
  - Component: `transfer_reversal`
  - Filters:
    - `id` eq `path.id`
    - `transfer` eq `path.transfer`
  - Notes:
    - Response body references #/components/schemas/transfer_reversal
    - Query parameters: id, transfer
