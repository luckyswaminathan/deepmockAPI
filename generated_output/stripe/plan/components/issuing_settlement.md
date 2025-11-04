# Component Plan: `issuing.settlement`

**API Slug:** `stripe`
**Total Routes:** 3

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /v1/issuing/settlements/{settlement}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `issuing.settlement`
  - Filters:
    - `network_settlement_identifier` eq `path.settlement`
  - Notes:
    - Response body references #/components/schemas/issuing.settlement
    - Query parameters: expand

### POST Routes (2)

#### `POST /v1/issuing/settlements/{settlement}`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.settlement`
  - Filters:
    - `network_settlement_identifier` eq `path.settlement`
  - Notes:
    - Response body references #/components/schemas/issuing.settlement
    - Query parameters: settlement

#### `POST /v1/test_helpers/issuing/settlements`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.settlement`
  - Notes:
    - Response body references #/components/schemas/issuing.settlement
