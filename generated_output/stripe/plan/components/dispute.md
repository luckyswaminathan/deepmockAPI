# Component Plan: `dispute`

**API Slug:** `stripe`
**Total Routes:** 8

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.

## Routes

### GET Routes (4)

#### `GET /v1/charges/{charge}/dispute`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `dispute`
  - Filters:
    - `charge` eq `path.charge`
  - Notes:
    - Response body references #/components/schemas/dispute
    - Query parameters: expand

#### `GET /v1/disputes`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `dispute`
  - Notes:
    - Query parameters: charge, created, ending_before, expand, limit, payment_intent, starting_after

#### `GET /v1/disputes/{dispute}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `dispute`
  - Filters:
    - `dispute` eq `path.dispute`
  - Notes:
    - Response body references #/components/schemas/dispute
    - Query parameters: expand

#### `GET /v1/issuing/disputes`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `dispute`
  - Notes:
    - Query parameters: created, ending_before, expand, limit, starting_after, status, transaction

### POST Routes (4)

#### `POST /v1/charges/{charge}/dispute`
**Status:** planned

**Operations:**
- **create**
  - Component: `dispute`
  - Filters:
    - `charge` eq `path.charge`
  - Notes:
    - Response body references #/components/schemas/dispute
    - Query parameters: charge

#### `POST /v1/charges/{charge}/dispute/close`
**Status:** planned

**Operations:**
- **create**
  - Component: `dispute`
  - Filters:
    - `charge` eq `path.charge`
  - Notes:
    - Response body references #/components/schemas/dispute
    - Query parameters: charge

#### `POST /v1/disputes/{dispute}`
**Status:** planned

**Operations:**
- **create**
  - Component: `dispute`
  - Filters:
    - `dispute` eq `path.dispute`
  - Notes:
    - Response body references #/components/schemas/dispute
    - Query parameters: dispute

#### `POST /v1/disputes/{dispute}/close`
**Status:** planned

**Operations:**
- **create**
  - Component: `dispute`
  - Filters:
    - `dispute` eq `path.dispute`
  - Notes:
    - Response body references #/components/schemas/dispute
    - Query parameters: dispute
