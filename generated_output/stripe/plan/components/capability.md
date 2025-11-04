# Component Plan: `capability`

**API Slug:** `stripe`
**Total Routes:** 3

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (2)

#### `GET /v1/accounts/{account}/capabilities`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `capability`
  - Filters:
    - `account` eq `path.account`
  - Notes:
    - Query parameters: expand

#### `GET /v1/accounts/{account}/capabilities/{capability}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `capability`
  - Filters:
    - `account` eq `path.account`
    - `capability` eq `path.capability`
  - Notes:
    - Response body references #/components/schemas/capability
    - Query parameters: expand

### POST Routes (1)

#### `POST /v1/accounts/{account}/capabilities/{capability}`
**Status:** planned

**Operations:**
- **create**
  - Component: `capability`
  - Filters:
    - `account` eq `path.account`
    - `capability` eq `path.capability`
  - Notes:
    - Response body references #/components/schemas/capability
    - Query parameters: account, capability
