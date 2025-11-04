# Component Plan: `plan`

**API Slug:** `stripe`
**Total Routes:** 5

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (1)

#### `DELETE /v1/plans/{plan}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `plan`
  - Filters:
    - `plan` eq `path.plan`
  - Notes:
    - Query parameters: plan

### GET Routes (2)

#### `GET /v1/plans`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `plan`
  - Notes:
    - Query parameters: active, created, ending_before, expand, limit, product, starting_after

#### `GET /v1/plans/{plan}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `plan`
  - Filters:
    - `plan` eq `path.plan`
  - Notes:
    - Response body references #/components/schemas/plan
    - Query parameters: expand

### POST Routes (2)

#### `POST /v1/plans`
**Status:** planned

**Operations:**
- **create**
  - Component: `plan`
  - Notes:
    - Response body references #/components/schemas/plan

#### `POST /v1/plans/{plan}`
**Status:** planned

**Operations:**
- **create**
  - Component: `plan`
  - Filters:
    - `plan` eq `path.plan`
  - Notes:
    - Response body references #/components/schemas/plan
    - Query parameters: plan
