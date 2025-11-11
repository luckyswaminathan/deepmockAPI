# Component Plan: `combined-billing-usage`

**API Slug:** `github`
**Total Routes:** 2

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (2)

#### `GET /orgs/{org}/settings/billing/shared-storage`
**Summary:** Get shared storage billing for an organization
**Status:** planned

**Operations:**
- **read_one**
  - Component: `combined-billing-usage`
  - Filters:
    - `org` eq `path.org`
  - Notes:
    - Response body references #/components/schemas/combined-billing-usage

#### `GET /users/{username}/settings/billing/shared-storage`
**Summary:** Get shared storage billing for a user
**Status:** planned

**Operations:**
- **read_one**
  - Component: `combined-billing-usage`
  - Filters:
    - `username` eq `path.username`
  - Notes:
    - Response body references #/components/schemas/combined-billing-usage
