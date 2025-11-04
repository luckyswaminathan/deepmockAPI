# Component Plan: `external_account`

**API Slug:** `stripe`
**Total Routes:** 8

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (1)

#### `DELETE /v1/accounts/{account}/external_accounts/{id}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `external_account`
  - Filters:
    - `account` eq `path.account`
    - `id` eq `path.id`
  - Notes:
    - Query parameters: account, id

### GET Routes (3)

#### `GET /v1/accounts/{account}/bank_accounts/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `external_account`
  - Filters:
    - `account` eq `path.account`
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/external_account
    - Query parameters: expand

#### `GET /v1/accounts/{account}/external_accounts`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `external_account`
  - Filters:
    - `account` eq `path.account`
  - Notes:
    - Query parameters: ending_before, expand, limit, object, starting_after

#### `GET /v1/accounts/{account}/external_accounts/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `external_account`
  - Filters:
    - `account` eq `path.account`
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/external_account
    - Query parameters: expand

### POST Routes (4)

#### `POST /v1/accounts/{account}/bank_accounts`
**Status:** planned

**Operations:**
- **create**
  - Component: `external_account`
  - Filters:
    - `account` eq `path.account`
  - Notes:
    - Response body references #/components/schemas/external_account
    - Query parameters: account

#### `POST /v1/accounts/{account}/bank_accounts/{id}`
**Status:** planned

**Operations:**
- **create**
  - Component: `external_account`
  - Filters:
    - `account` eq `path.account`
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/external_account
    - Query parameters: account, id

#### `POST /v1/accounts/{account}/external_accounts`
**Status:** planned

**Operations:**
- **create**
  - Component: `external_account`
  - Filters:
    - `account` eq `path.account`
  - Notes:
    - Response body references #/components/schemas/external_account
    - Query parameters: account

#### `POST /v1/accounts/{account}/external_accounts/{id}`
**Status:** planned

**Operations:**
- **create**
  - Component: `external_account`
  - Filters:
    - `account` eq `path.account`
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/external_account
    - Query parameters: account, id
