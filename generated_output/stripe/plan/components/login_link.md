# Component Plan: `login_link`

**API Slug:** `stripe`
**Total Routes:** 1

## Supported Operations
- **`create`**: Create a new record for the component.

## Routes

### POST Routes (1)

#### `POST /v1/accounts/{account}/login_links`
**Status:** planned

**Operations:**
- **create**
  - Component: `login_link`
  - Filters:
    - `account` eq `path.account`
  - Notes:
    - Response body references #/components/schemas/login_link
    - Query parameters: account
