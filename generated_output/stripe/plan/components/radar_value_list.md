# Component Plan: `radar.value_list`

**API Slug:** `stripe`
**Total Routes:** 3

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /v1/radar/value_lists/{value_list}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `radar.value_list`
  - Filters:
    - `value_list` eq `path.value_list`
  - Notes:
    - Response body references #/components/schemas/radar.value_list
    - Query parameters: expand

### POST Routes (2)

#### `POST /v1/radar/value_lists`
**Status:** planned

**Operations:**
- **create**
  - Component: `radar.value_list`
  - Notes:
    - Response body references #/components/schemas/radar.value_list

#### `POST /v1/radar/value_lists/{value_list}`
**Status:** planned

**Operations:**
- **create**
  - Component: `radar.value_list`
  - Filters:
    - `value_list` eq `path.value_list`
  - Notes:
    - Response body references #/components/schemas/radar.value_list
    - Query parameters: value_list
