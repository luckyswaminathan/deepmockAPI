# Component Plan: `issuing.dispute`

**API Slug:** `stripe`
**Total Routes:** 4

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /v1/issuing/disputes/{dispute}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `issuing.dispute`
  - Filters:
    - `dispute` eq `path.dispute`
  - Notes:
    - Response body references #/components/schemas/issuing.dispute
    - Query parameters: expand

### POST Routes (3)

#### `POST /v1/issuing/disputes`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.dispute`
  - Notes:
    - Response body references #/components/schemas/issuing.dispute

#### `POST /v1/issuing/disputes/{dispute}`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.dispute`
  - Filters:
    - `dispute` eq `path.dispute`
  - Notes:
    - Response body references #/components/schemas/issuing.dispute
    - Query parameters: dispute

#### `POST /v1/issuing/disputes/{dispute}/submit`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.dispute`
  - Filters:
    - `dispute` eq `path.dispute`
  - Notes:
    - Response body references #/components/schemas/issuing.dispute
    - Query parameters: dispute
