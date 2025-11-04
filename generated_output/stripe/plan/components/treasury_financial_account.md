# Component Plan: `treasury.financial_account`

**API Slug:** `stripe`
**Total Routes:** 3

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /v1/treasury/financial_accounts/{financial_account}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `treasury.financial_account`
  - Filters:
    - `financial_account` eq `path.financial_account`
  - Notes:
    - Response body references #/components/schemas/treasury.financial_account
    - Query parameters: expand

### POST Routes (2)

#### `POST /v1/treasury/financial_accounts`
**Status:** planned

**Operations:**
- **create**
  - Component: `treasury.financial_account`
  - Notes:
    - Response body references #/components/schemas/treasury.financial_account

#### `POST /v1/treasury/financial_accounts/{financial_account}`
**Status:** planned

**Operations:**
- **create**
  - Component: `treasury.financial_account`
  - Filters:
    - `financial_account` eq `path.financial_account`
  - Notes:
    - Response body references #/components/schemas/treasury.financial_account
    - Query parameters: financial_account
