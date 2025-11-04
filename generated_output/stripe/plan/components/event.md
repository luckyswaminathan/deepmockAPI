# Component Plan: `event`

**API Slug:** `stripe`
**Total Routes:** 2

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.

## Routes

### GET Routes (2)

#### `GET /v1/events`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `event`
  - Notes:
    - Query parameters: created, delivery_success, ending_before, expand, limit, starting_after, type, types

#### `GET /v1/events/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `event`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/event
    - Query parameters: expand
