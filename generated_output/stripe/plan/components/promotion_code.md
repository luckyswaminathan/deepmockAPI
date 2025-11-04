# Component Plan: `promotion_code`

**API Slug:** `stripe`
**Total Routes:** 4

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.

## Routes

### GET Routes (2)

#### `GET /v1/promotion_codes`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `promotion_code`
  - Notes:
    - Query parameters: active, code, coupon, created, customer, ending_before, expand, limit, starting_after

#### `GET /v1/promotion_codes/{promotion_code}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `promotion_code`
  - Filters:
    - `promotion_code` eq `path.promotion_code`
  - Notes:
    - Response body references #/components/schemas/promotion_code
    - Query parameters: expand

### POST Routes (2)

#### `POST /v1/promotion_codes`
**Status:** planned

**Operations:**
- **create**
  - Component: `promotion_code`
  - Notes:
    - Response body references #/components/schemas/promotion_code

#### `POST /v1/promotion_codes/{promotion_code}`
**Status:** planned

**Operations:**
- **create**
  - Component: `promotion_code`
  - Filters:
    - `promotion_code` eq `path.promotion_code`
  - Notes:
    - Response body references #/components/schemas/promotion_code
    - Query parameters: promotion_code
