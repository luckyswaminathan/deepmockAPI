# Component Plan: `packages-billing-usage`

**API Slug:** `github`
**Total Routes:** 2

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (2)

#### `GET /orgs/{org}/settings/billing/packages`
**Summary:** Get GitHub Packages billing for an organization
**Status:** planned

**Operations:**
- **read_one**
  - Component: `packages-billing-usage`
  - Filters:
    - `org` eq `path.org`
  - Notes:
    - Response body references #/components/schemas/packages-billing-usage

#### `GET /users/{username}/settings/billing/packages`
**Summary:** Get GitHub Packages billing for a user
**Status:** planned

**Operations:**
- **read_one**
  - Component: `packages-billing-usage`
  - Filters:
    - `username` eq `path.username`
  - Notes:
    - Response body references #/components/schemas/packages-billing-usage
