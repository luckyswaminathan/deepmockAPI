# Component Plan: `coupon`

**API Slug:** `stripe`
**Total Routes:** 5

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (1)

#### `DELETE /v1/coupons/{coupon}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `coupon`
  - Filters:
    - `coupon` eq `path.coupon`
  - Notes:
    - Query parameters: coupon

### GET Routes (2)

#### `GET /v1/coupons`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `coupon`
  - Notes:
    - Query parameters: created, ending_before, expand, limit, starting_after

#### `GET /v1/coupons/{coupon}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `coupon`
  - Filters:
    - `coupon` eq `path.coupon`
  - Notes:
    - Response body references #/components/schemas/coupon
    - Query parameters: expand

### POST Routes (2)

#### `POST /v1/coupons`
**Status:** planned

**Operations:**
- **create**
  - Component: `coupon`
  - Notes:
    - Response body references #/components/schemas/coupon

#### `POST /v1/coupons/{coupon}`
**Status:** planned

**Operations:**
- **create**
  - Component: `coupon`
  - Filters:
    - `coupon` eq `path.coupon`
  - Notes:
    - Response body references #/components/schemas/coupon
    - Query parameters: coupon
