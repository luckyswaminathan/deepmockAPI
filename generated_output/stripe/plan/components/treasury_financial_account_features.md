# Component Plan: `treasury.financial_account_features`

**API Slug:** `stripe`
**Total Routes:** 2

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /v1/treasury/financial_accounts/{financial_account}/features`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `treasury.financial_account_features`
  - Filters:
    - `financial_account` eq `path.financial_account`
  - Notes:
    - Response body references #/components/schemas/treasury.financial_account_features
    - Query parameters: expand

### POST Routes (1)

#### `POST /v1/treasury/financial_accounts/{financial_account}/features`
**Status:** planned

**Operations:**
- **create**
  - Component: `treasury.financial_account_features`
  - Filters:
    - `financial_account` eq `path.financial_account`
  - Notes:
    - Response body references #/components/schemas/treasury.financial_account_features
    - Query parameters: financial_account
