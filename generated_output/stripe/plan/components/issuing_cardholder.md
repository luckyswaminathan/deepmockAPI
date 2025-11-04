# Component Plan: `issuing.cardholder`

**API Slug:** `stripe`
**Total Routes:** 3

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /v1/issuing/cardholders/{cardholder}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `issuing.cardholder`
  - Filters:
    - `cardholder` eq `path.cardholder`
  - Notes:
    - Response body references #/components/schemas/issuing.cardholder
    - Query parameters: expand

### POST Routes (2)

#### `POST /v1/issuing/cardholders`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.cardholder`
  - Notes:
    - Response body references #/components/schemas/issuing.cardholder

#### `POST /v1/issuing/cardholders/{cardholder}`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.cardholder`
  - Filters:
    - `cardholder` eq `path.cardholder`
  - Notes:
    - Response body references #/components/schemas/issuing.cardholder
    - Query parameters: cardholder
