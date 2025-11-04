# Component Plan: `organization-role`

**API Slug:** `github`
**Total Routes:** 2

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (2)

#### `GET /orgs/{org}/organization-roles`
**Summary:** Get all organization roles for an organization
**Status:** planned

**Operations:**
- **read_one**
  - Component: `organization-role`
  - Filters:
    - `org` eq `path.org`

#### `GET /orgs/{org}/organization-roles/{role_id}`
**Summary:** Get an organization role
**Status:** planned

**Operations:**
- **read_one**
  - Component: `organization-role`
  - Filters:
    - `org` eq `path.org`
    - `role_id` eq `path.role_id`
  - Notes:
    - Response body references #/components/schemas/organization-role
