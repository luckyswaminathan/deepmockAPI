# Component Plan: `marketplace-purchase`

**API Slug:** `github`
**Total Routes:** 2

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (2)

#### `GET /marketplace_listing/accounts/{account_id}`
**Summary:** Get a subscription plan for an account
**Status:** planned

**Operations:**
- **read_one**
  - Component: `marketplace-purchase`
  - Filters:
    - `account_id` eq `path.account_id`
  - Notes:
    - Response body references #/components/schemas/marketplace-purchase

#### `GET /marketplace_listing/stubbed/accounts/{account_id}`
**Summary:** Get a subscription plan for an account (stubbed)
**Status:** planned

**Operations:**
- **read_one**
  - Component: `marketplace-purchase`
  - Filters:
    - `account_id` eq `path.account_id`
  - Notes:
    - Response body references #/components/schemas/marketplace-purchase
