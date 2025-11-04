# Component Plan: `organization-actions-variable`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /orgs/{org}/actions/variables/{name}`
**Summary:** Get an organization variable
**Status:** planned

**Operations:**
- **read_one**
  - Component: `organization-actions-variable`
  - Filters:
    - `org` eq `path.org`
    - `name` eq `path.name`
  - Notes:
    - Response body references #/components/schemas/organization-actions-variable
