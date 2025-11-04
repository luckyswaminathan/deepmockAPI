# Component Plan: `shipping_rate`

**API Slug:** `stripe`
**Total Routes:** 4

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.

## Routes

### GET Routes (2)

#### `GET /v1/shipping_rates`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `shipping_rate`
  - Notes:
    - Query parameters: active, created, currency, ending_before, expand, limit, starting_after

#### `GET /v1/shipping_rates/{shipping_rate_token}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `shipping_rate`
  - Filters:
    - `shipping_rate_token` eq `path.shipping_rate_token`
  - Notes:
    - Response body references #/components/schemas/shipping_rate
    - Query parameters: expand

### POST Routes (2)

#### `POST /v1/shipping_rates`
**Status:** planned

**Operations:**
- **create**
  - Component: `shipping_rate`
  - Notes:
    - Response body references #/components/schemas/shipping_rate

#### `POST /v1/shipping_rates/{shipping_rate_token}`
**Status:** planned

**Operations:**
- **create**
  - Component: `shipping_rate`
  - Filters:
    - `shipping_rate_token` eq `path.shipping_rate_token`
  - Notes:
    - Response body references #/components/schemas/shipping_rate
    - Query parameters: shipping_rate_token
