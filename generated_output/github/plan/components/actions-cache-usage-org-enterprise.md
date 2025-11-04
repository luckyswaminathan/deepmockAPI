# Component Plan: `actions-cache-usage-org-enterprise`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /orgs/{org}/actions/cache/usage`
**Summary:** Get GitHub Actions cache usage for an organization
**Status:** planned

**Operations:**
- **read_one**
  - Component: `actions-cache-usage-org-enterprise`
  - Filters:
    - `org` eq `path.org`
  - Notes:
    - Response body references #/components/schemas/actions-cache-usage-org-enterprise
