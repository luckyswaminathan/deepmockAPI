# Component Plan: `organization-dependabot-secret`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /orgs/{org}/dependabot/secrets/{secret_name}`
**Summary:** Get an organization secret
**Status:** planned

**Operations:**
- **read_one**
  - Component: `organization-dependabot-secret`
  - Filters:
    - `org` eq `path.org`
    - `secret_name` eq `path.secret_name`
  - Notes:
    - Response body references #/components/schemas/organization-dependabot-secret
