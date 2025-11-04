# Component Plan: `fee_refund`

**API Slug:** `stripe`
**Total Routes:** 3

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /v1/application_fees/{fee}/refunds/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `fee_refund`
  - Filters:
    - `fee` eq `path.fee`
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/fee_refund
    - Query parameters: expand

### POST Routes (2)

#### `POST /v1/application_fees/{fee}/refunds/{id}`
**Status:** planned

**Operations:**
- **create**
  - Component: `fee_refund`
  - Filters:
    - `fee` eq `path.fee`
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/fee_refund
    - Query parameters: fee, id

#### `POST /v1/application_fees/{id}/refunds`
**Status:** planned

**Operations:**
- **create**
  - Component: `fee_refund`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/fee_refund
    - Query parameters: id
