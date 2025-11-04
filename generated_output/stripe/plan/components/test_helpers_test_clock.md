# Component Plan: `test_helpers.test_clock`

**API Slug:** `stripe`
**Total Routes:** 3

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /v1/test_helpers/test_clocks/{test_clock}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `test_helpers.test_clock`
  - Filters:
    - `test_clock` eq `path.test_clock`
  - Notes:
    - Response body references #/components/schemas/test_helpers.test_clock
    - Query parameters: expand

### POST Routes (2)

#### `POST /v1/test_helpers/test_clocks`
**Status:** planned

**Operations:**
- **create**
  - Component: `test_helpers.test_clock`
  - Notes:
    - Response body references #/components/schemas/test_helpers.test_clock

#### `POST /v1/test_helpers/test_clocks/{test_clock}/advance`
**Status:** planned

**Operations:**
- **create**
  - Component: `test_helpers.test_clock`
  - Filters:
    - `test_clock` eq `path.test_clock`
  - Notes:
    - Response body references #/components/schemas/test_helpers.test_clock
    - Query parameters: test_clock
