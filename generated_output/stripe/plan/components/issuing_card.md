# Component Plan: `issuing.card`

**API Slug:** `stripe`
**Total Routes:** 7

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /v1/issuing/cards/{card}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `issuing.card`
  - Filters:
    - `cardholder` eq `path.card`
  - Notes:
    - Response body references #/components/schemas/issuing.card
    - Query parameters: expand

### POST Routes (6)

#### `POST /v1/issuing/cards`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.card`
  - Notes:
    - Response body references #/components/schemas/issuing.card

#### `POST /v1/issuing/cards/{card}`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.card`
  - Filters:
    - `cardholder` eq `path.card`
  - Notes:
    - Response body references #/components/schemas/issuing.card
    - Query parameters: card

#### `POST /v1/test_helpers/issuing/cards/{card}/shipping/deliver`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.card`
  - Filters:
    - `cardholder` eq `path.card`
  - Notes:
    - Response body references #/components/schemas/issuing.card
    - Query parameters: card

#### `POST /v1/test_helpers/issuing/cards/{card}/shipping/fail`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.card`
  - Filters:
    - `cardholder` eq `path.card`
  - Notes:
    - Response body references #/components/schemas/issuing.card
    - Query parameters: card

#### `POST /v1/test_helpers/issuing/cards/{card}/shipping/return`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.card`
  - Filters:
    - `cardholder` eq `path.card`
  - Notes:
    - Response body references #/components/schemas/issuing.card
    - Query parameters: card

#### `POST /v1/test_helpers/issuing/cards/{card}/shipping/ship`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.card`
  - Filters:
    - `cardholder` eq `path.card`
  - Notes:
    - Response body references #/components/schemas/issuing.card
    - Query parameters: card
