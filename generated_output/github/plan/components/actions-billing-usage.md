# Component Plan: `actions-billing-usage`

**API Slug:** `github`
**Total Routes:** 2

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (2)

#### `GET /orgs/{org}/settings/billing/actions`
**Summary:** Get GitHub Actions billing for an organization
**Status:** planned

**Operations:**
- **read_one**
  - Component: `actions-billing-usage`
  - Filters:
    - `org` eq `path.org`
  - Notes:
    - Response body references #/components/schemas/actions-billing-usage

#### `GET /users/{username}/settings/billing/actions`
**Summary:** Get GitHub Actions billing for a user
**Status:** planned

**Operations:**
- **read_one**
  - Component: `actions-billing-usage`
  - Filters:
    - `username` eq `path.username`
  - Notes:
    - Response body references #/components/schemas/actions-billing-usage
