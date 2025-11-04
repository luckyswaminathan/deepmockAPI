# Component Plan: `financial_connections.account`

**API Slug:** `stripe`
**Total Routes:** 8

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (2)

#### `GET /v1/financial_connections/accounts/{account}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `financial_connections.account`
  - Filters:
    - `account` eq `path.account`
  - Notes:
    - Response body references #/components/schemas/financial_connections.account
    - Query parameters: expand

#### `GET /v1/linked_accounts/{account}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `financial_connections.account`
  - Filters:
    - `account` eq `path.account`
  - Notes:
    - Response body references #/components/schemas/financial_connections.account
    - Query parameters: expand

### POST Routes (6)

#### `POST /v1/financial_connections/accounts/{account}/disconnect`
**Status:** planned

**Operations:**
- **create**
  - Component: `financial_connections.account`
  - Filters:
    - `account` eq `path.account`
  - Notes:
    - Response body references #/components/schemas/financial_connections.account
    - Query parameters: account

#### `POST /v1/financial_connections/accounts/{account}/refresh`
**Status:** planned

**Operations:**
- **create**
  - Component: `financial_connections.account`
  - Filters:
    - `account` eq `path.account`
  - Notes:
    - Response body references #/components/schemas/financial_connections.account
    - Query parameters: account

#### `POST /v1/financial_connections/accounts/{account}/subscribe`
**Status:** planned

**Operations:**
- **create**
  - Component: `financial_connections.account`
  - Filters:
    - `account` eq `path.account`
  - Notes:
    - Response body references #/components/schemas/financial_connections.account
    - Query parameters: account

#### `POST /v1/financial_connections/accounts/{account}/unsubscribe`
**Status:** planned

**Operations:**
- **create**
  - Component: `financial_connections.account`
  - Filters:
    - `account` eq `path.account`
  - Notes:
    - Response body references #/components/schemas/financial_connections.account
    - Query parameters: account

#### `POST /v1/linked_accounts/{account}/disconnect`
**Status:** planned

**Operations:**
- **create**
  - Component: `financial_connections.account`
  - Filters:
    - `account` eq `path.account`
  - Notes:
    - Response body references #/components/schemas/financial_connections.account
    - Query parameters: account

#### `POST /v1/linked_accounts/{account}/refresh`
**Status:** planned

**Operations:**
- **create**
  - Component: `financial_connections.account`
  - Filters:
    - `account` eq `path.account`
  - Notes:
    - Response body references #/components/schemas/financial_connections.account
    - Query parameters: account
