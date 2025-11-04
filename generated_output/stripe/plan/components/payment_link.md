# Component Plan: `payment_link`

**API Slug:** `stripe`
**Total Routes:** 4

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.

## Routes

### GET Routes (2)

#### `GET /v1/payment_links`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `payment_link`
  - Notes:
    - Query parameters: active, ending_before, expand, limit, starting_after

#### `GET /v1/payment_links/{payment_link}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `payment_link`
  - Filters:
    - `payment_link` eq `path.payment_link`
  - Notes:
    - Response body references #/components/schemas/payment_link
    - Query parameters: expand

### POST Routes (2)

#### `POST /v1/payment_links`
**Status:** planned

**Operations:**
- **create**
  - Component: `payment_link`
  - Notes:
    - Response body references #/components/schemas/payment_link

#### `POST /v1/payment_links/{payment_link}`
**Status:** planned

**Operations:**
- **create**
  - Component: `payment_link`
  - Filters:
    - `payment_link` eq `path.payment_link`
  - Notes:
    - Response body references #/components/schemas/payment_link
    - Query parameters: payment_link
