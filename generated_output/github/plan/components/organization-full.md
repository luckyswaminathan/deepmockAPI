# Component Plan: `organization-full`

**API Slug:** `github`
**Total Routes:** 2

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.
- **`update_partial`**: Apply a partial update to a record.

## Routes

### GET Routes (1)

#### `GET /orgs/{org}`
**Summary:** Get an organization
**Status:** planned

**Operations:**
- **read_one**
  - Component: `organization-full`
  - Filters:
    - `org` eq `path.org`
  - Notes:
    - Response body references #/components/schemas/organization-full

### PATCH Routes (1)

#### `PATCH /orgs/{org}`
**Summary:** Update an organization
**Status:** planned

**Operations:**
- **update_partial**
  - Component: `organization-full`
  - Filters:
    - `org` eq `path.org`
  - Notes:
    - Response body references #/components/schemas/organization-full
