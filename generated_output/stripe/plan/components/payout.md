# Component Plan: `payout`

**API Slug:** `stripe`
**Total Routes:** 6

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.

## Routes

### GET Routes (2)

#### `GET /v1/payouts`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `payout`
  - Notes:
    - Query parameters: arrival_date, created, destination, ending_before, expand, limit, starting_after, status

#### `GET /v1/payouts/{payout}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `payout`
  - Filters:
    - `original_payout` eq `path.payout`
  - Notes:
    - Response body references #/components/schemas/payout
    - Query parameters: expand

### POST Routes (4)

#### `POST /v1/payouts`
**Status:** planned

**Operations:**
- **create**
  - Component: `payout`
  - Notes:
    - Response body references #/components/schemas/payout

#### `POST /v1/payouts/{payout}`
**Status:** planned

**Operations:**
- **create**
  - Component: `payout`
  - Filters:
    - `original_payout` eq `path.payout`
  - Notes:
    - Response body references #/components/schemas/payout
    - Query parameters: payout

#### `POST /v1/payouts/{payout}/cancel`
**Status:** planned

**Operations:**
- **create**
  - Component: `payout`
  - Filters:
    - `original_payout` eq `path.payout`
  - Notes:
    - Response body references #/components/schemas/payout
    - Query parameters: payout

#### `POST /v1/payouts/{payout}/reverse`
**Status:** planned

**Operations:**
- **create**
  - Component: `payout`
  - Filters:
    - `original_payout` eq `path.payout`
  - Notes:
    - Response body references #/components/schemas/payout
    - Query parameters: payout
