# Component Plan: `topup`

**API Slug:** `stripe`
**Total Routes:** 5

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.

## Routes

### GET Routes (2)

#### `GET /v1/topups`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `topup`
  - Notes:
    - Query parameters: amount, created, ending_before, expand, limit, starting_after, status

#### `GET /v1/topups/{topup}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `topup`
  - Filters:
    - `topup` eq `path.topup`
  - Notes:
    - Response body references #/components/schemas/topup
    - Query parameters: expand

### POST Routes (3)

#### `POST /v1/topups`
**Status:** planned

**Operations:**
- **create**
  - Component: `topup`
  - Notes:
    - Response body references #/components/schemas/topup

#### `POST /v1/topups/{topup}`
**Status:** planned

**Operations:**
- **create**
  - Component: `topup`
  - Filters:
    - `topup` eq `path.topup`
  - Notes:
    - Response body references #/components/schemas/topup
    - Query parameters: topup

#### `POST /v1/topups/{topup}/cancel`
**Status:** planned

**Operations:**
- **create**
  - Component: `topup`
  - Filters:
    - `topup` eq `path.topup`
  - Notes:
    - Response body references #/components/schemas/topup
    - Query parameters: topup
