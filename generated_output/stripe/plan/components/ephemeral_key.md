# Component Plan: `ephemeral_key`

**API Slug:** `stripe`
**Total Routes:** 2

## Supported Operations
- **`create`**: Create a new record for the component.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (1)

#### `DELETE /v1/ephemeral_keys/{key}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `ephemeral_key`
  - Filters:
    - `id` eq `path.key`
  - Notes:
    - Response body references #/components/schemas/ephemeral_key
    - Query parameters: key

### POST Routes (1)

#### `POST /v1/ephemeral_keys`
**Status:** planned

**Operations:**
- **create**
  - Component: `ephemeral_key`
  - Notes:
    - Response body references #/components/schemas/ephemeral_key
