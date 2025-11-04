# Component Plan: `radar.value_list_item`

**API Slug:** `stripe`
**Total Routes:** 2

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /v1/radar/value_list_items/{item}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `radar.value_list_item`
  - Filters:
    - `item` eq `path.item`
  - Notes:
    - Response body references #/components/schemas/radar.value_list_item
    - Query parameters: expand

### POST Routes (1)

#### `POST /v1/radar/value_list_items`
**Status:** planned

**Operations:**
- **create**
  - Component: `radar.value_list_item`
  - Notes:
    - Response body references #/components/schemas/radar.value_list_item
