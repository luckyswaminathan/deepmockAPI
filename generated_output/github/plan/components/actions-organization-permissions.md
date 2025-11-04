# Component Plan: `actions-organization-permissions`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /orgs/{org}/actions/permissions`
**Summary:** Get GitHub Actions permissions for an organization
**Status:** planned

**Operations:**
- **read_one**
  - Component: `actions-organization-permissions`
  - Filters:
    - `org` eq `path.org`
  - Notes:
    - Response body references #/components/schemas/actions-organization-permissions
