# Component Plan: `application_fee`

**API Slug:** `stripe`
**Total Routes:** 3

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.

## Routes

### GET Routes (2)

#### `GET /v1/application_fees`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `application_fee`
  - Notes:
    - Query parameters: charge, created, ending_before, expand, limit, starting_after

#### `GET /v1/application_fees/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `application_fee`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/application_fee
    - Query parameters: expand

### POST Routes (1)

#### `POST /v1/application_fees/{id}/refund`
**Status:** planned

**Operations:**
- **create**
  - Component: `application_fee`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/application_fee
    - Query parameters: id
