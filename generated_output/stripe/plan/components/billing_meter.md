# Component Plan: `billing.meter`

**API Slug:** `stripe`
**Total Routes:** 5

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /v1/billing/meters/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `billing.meter`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/billing.meter
    - Query parameters: expand

### POST Routes (4)

#### `POST /v1/billing/meters`
**Status:** planned

**Operations:**
- **create**
  - Component: `billing.meter`
  - Notes:
    - Response body references #/components/schemas/billing.meter

#### `POST /v1/billing/meters/{id}`
**Status:** planned

**Operations:**
- **create**
  - Component: `billing.meter`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/billing.meter
    - Query parameters: id

#### `POST /v1/billing/meters/{id}/deactivate`
**Status:** planned

**Operations:**
- **create**
  - Component: `billing.meter`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/billing.meter
    - Query parameters: id

#### `POST /v1/billing/meters/{id}/reactivate`
**Status:** planned

**Operations:**
- **create**
  - Component: `billing.meter`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/billing.meter
    - Query parameters: id
