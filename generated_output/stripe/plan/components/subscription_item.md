# Component Plan: `subscription_item`

**API Slug:** `stripe`
**Total Routes:** 5

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (1)

#### `DELETE /v1/subscription_items/{item}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `subscription_item`
  - Filters:
    - `item` eq `path.item`
  - Notes:
    - Query parameters: item

### GET Routes (2)

#### `GET /v1/subscription_items`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `subscription_item`
  - Notes:
    - Query parameters: ending_before, expand, limit, starting_after, subscription

#### `GET /v1/subscription_items/{item}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `subscription_item`
  - Filters:
    - `item` eq `path.item`
  - Notes:
    - Response body references #/components/schemas/subscription_item
    - Query parameters: expand

### POST Routes (2)

#### `POST /v1/subscription_items`
**Status:** planned

**Operations:**
- **create**
  - Component: `subscription_item`
  - Notes:
    - Response body references #/components/schemas/subscription_item

#### `POST /v1/subscription_items/{item}`
**Status:** planned

**Operations:**
- **create**
  - Component: `subscription_item`
  - Filters:
    - `item` eq `path.item`
  - Notes:
    - Response body references #/components/schemas/subscription_item
    - Query parameters: item
