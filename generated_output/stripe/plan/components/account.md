# Component Plan: `account`

**API Slug:** `stripe`
**Total Routes:** 8

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (1)

#### `DELETE /v1/accounts/{account}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `account`
  - Filters:
    - `account` eq `path.account`
  - Notes:
    - Query parameters: account

### GET Routes (4)

#### `GET /v1/account`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `account`
  - Notes:
    - Response body references #/components/schemas/account
    - Query parameters: expand

#### `GET /v1/accounts`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `account`
  - Notes:
    - Query parameters: created, ending_before, expand, limit, starting_after

#### `GET /v1/accounts/{account}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `account`
  - Filters:
    - `account` eq `path.account`
  - Notes:
    - Response body references #/components/schemas/account
    - Query parameters: expand

#### `GET /v1/financial_connections/accounts`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `account`
  - Notes:
    - Query parameters: account_holder, ending_before, expand, limit, session, starting_after

### POST Routes (3)

#### `POST /v1/accounts`
**Status:** planned

**Operations:**
- **create**
  - Component: `account`
  - Notes:
    - Response body references #/components/schemas/account

#### `POST /v1/accounts/{account}`
**Status:** planned

**Operations:**
- **create**
  - Component: `account`
  - Filters:
    - `account` eq `path.account`
  - Notes:
    - Response body references #/components/schemas/account
    - Query parameters: account

#### `POST /v1/accounts/{account}/reject`
**Status:** planned

**Operations:**
- **create**
  - Component: `account`
  - Filters:
    - `account` eq `path.account`
  - Notes:
    - Response body references #/components/schemas/account
    - Query parameters: account
