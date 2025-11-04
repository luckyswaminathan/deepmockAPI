# Component Plan: `apple_pay_domain`

**API Slug:** `stripe`
**Total Routes:** 2

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /v1/apple_pay/domains/{domain}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `apple_pay_domain`
  - Filters:
    - `domain_name` eq `path.domain`
  - Notes:
    - Response body references #/components/schemas/apple_pay_domain
    - Query parameters: expand

### POST Routes (1)

#### `POST /v1/apple_pay/domains`
**Status:** planned

**Operations:**
- **create**
  - Component: `apple_pay_domain`
  - Notes:
    - Response body references #/components/schemas/apple_pay_domain
