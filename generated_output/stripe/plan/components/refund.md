# Component Plan: `refund`

**API Slug:** `stripe`
**Total Routes:** 11

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.

## Routes

### GET Routes (5)

#### `GET /v1/application_fees/{id}/refunds`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `refund`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Query parameters: ending_before, expand, limit, starting_after

#### `GET /v1/charges/{charge}/refunds`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `refund`
  - Filters:
    - `charge` eq `path.charge`
  - Notes:
    - Query parameters: ending_before, expand, limit, starting_after

#### `GET /v1/charges/{charge}/refunds/{refund}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `refund`
  - Filters:
    - `charge` eq `path.charge`
    - `refund` eq `path.refund`
  - Notes:
    - Response body references #/components/schemas/refund
    - Query parameters: expand

#### `GET /v1/refunds`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `refund`
  - Notes:
    - Query parameters: charge, created, ending_before, expand, limit, payment_intent, starting_after

#### `GET /v1/refunds/{refund}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `refund`
  - Filters:
    - `refund` eq `path.refund`
  - Notes:
    - Response body references #/components/schemas/refund
    - Query parameters: expand

### POST Routes (6)

#### `POST /v1/charges/{charge}/refunds`
**Status:** planned

**Operations:**
- **create**
  - Component: `refund`
  - Filters:
    - `charge` eq `path.charge`
  - Notes:
    - Response body references #/components/schemas/refund
    - Query parameters: charge

#### `POST /v1/charges/{charge}/refunds/{refund}`
**Status:** planned

**Operations:**
- **create**
  - Component: `refund`
  - Filters:
    - `charge` eq `path.charge`
    - `refund` eq `path.refund`
  - Notes:
    - Response body references #/components/schemas/refund
    - Query parameters: charge, refund

#### `POST /v1/refunds`
**Status:** planned

**Operations:**
- **create**
  - Component: `refund`
  - Notes:
    - Response body references #/components/schemas/refund

#### `POST /v1/refunds/{refund}`
**Status:** planned

**Operations:**
- **create**
  - Component: `refund`
  - Filters:
    - `refund` eq `path.refund`
  - Notes:
    - Response body references #/components/schemas/refund
    - Query parameters: refund

#### `POST /v1/refunds/{refund}/cancel`
**Status:** planned

**Operations:**
- **create**
  - Component: `refund`
  - Filters:
    - `refund` eq `path.refund`
  - Notes:
    - Response body references #/components/schemas/refund
    - Query parameters: refund

#### `POST /v1/test_helpers/refunds/{refund}/expire`
**Status:** planned

**Operations:**
- **create**
  - Component: `refund`
  - Filters:
    - `refund` eq `path.refund`
  - Notes:
    - Response body references #/components/schemas/refund
    - Query parameters: refund
