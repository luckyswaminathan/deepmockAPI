# Component Plan: `price`

**API Slug:** `stripe`
**Total Routes:** 4

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.

## Routes

### GET Routes (2)

#### `GET /v1/prices`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `price`
  - Notes:
    - Query parameters: active, created, currency, ending_before, expand, limit, lookup_keys, product, recurring, starting_after, type

#### `GET /v1/prices/{price}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `price`
  - Filters:
    - `price` eq `path.price`
  - Notes:
    - Response body references #/components/schemas/price
    - Query parameters: expand

### POST Routes (2)

#### `POST /v1/prices`
**Status:** planned

**Operations:**
- **create**
  - Component: `price`
  - Notes:
    - Response body references #/components/schemas/price

#### `POST /v1/prices/{price}`
**Status:** planned

**Operations:**
- **create**
  - Component: `price`
  - Filters:
    - `price` eq `path.price`
  - Notes:
    - Response body references #/components/schemas/price
    - Query parameters: price
