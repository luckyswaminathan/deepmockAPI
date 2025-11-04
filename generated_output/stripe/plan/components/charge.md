# Component Plan: `charge`

**API Slug:** `stripe`
**Total Routes:** 6

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.

## Routes

### GET Routes (2)

#### `GET /v1/charges`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `charge`
  - Notes:
    - Query parameters: created, customer, ending_before, expand, limit, payment_intent, starting_after, transfer_group

#### `GET /v1/charges/{charge}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `charge`
  - Filters:
    - `charge` eq `path.charge`
  - Notes:
    - Response body references #/components/schemas/charge
    - Query parameters: expand

### POST Routes (4)

#### `POST /v1/charges`
**Status:** planned

**Operations:**
- **create**
  - Component: `charge`
  - Notes:
    - Response body references #/components/schemas/charge

#### `POST /v1/charges/{charge}`
**Status:** planned

**Operations:**
- **create**
  - Component: `charge`
  - Filters:
    - `charge` eq `path.charge`
  - Notes:
    - Response body references #/components/schemas/charge
    - Query parameters: charge

#### `POST /v1/charges/{charge}/capture`
**Status:** planned

**Operations:**
- **create**
  - Component: `charge`
  - Filters:
    - `charge` eq `path.charge`
  - Notes:
    - Response body references #/components/schemas/charge
    - Query parameters: charge

#### `POST /v1/charges/{charge}/refund`
**Status:** planned

**Operations:**
- **create**
  - Component: `charge`
  - Filters:
    - `charge` eq `path.charge`
  - Notes:
    - Response body references #/components/schemas/charge
    - Query parameters: charge
