# Component Plan: `codespaces-org-secret`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /orgs/{org}/codespaces/secrets/{secret_name}`
**Summary:** Get an organization secret
**Status:** planned

**Operations:**
- **read_one**
  - Component: `codespaces-org-secret`
  - Filters:
    - `org` eq `path.org`
    - `secret_name` eq `path.secret_name`
  - Notes:
    - Response body references #/components/schemas/codespaces-org-secret
