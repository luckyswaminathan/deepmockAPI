# Component Plan: `org-membership`

**API Slug:** `github`
**Total Routes:** 4

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.
- **`update`**: Replace a full record.
- **`update_partial`**: Apply a partial update to a record.

## Routes

### GET Routes (2)

#### `GET /orgs/{org}/memberships/{username}`
**Summary:** Get organization membership for a user
**Status:** planned

**Operations:**
- **read_one**
  - Component: `org-membership`
  - Filters:
    - `org` eq `path.org`
    - `username` eq `path.username`
  - Notes:
    - Response body references #/components/schemas/org-membership

#### `GET /user/memberships/orgs/{org}`
**Summary:** Get an organization membership for the authenticated user
**Status:** planned

**Operations:**
- **read_one**
  - Component: `org-membership`
  - Filters:
    - `org` eq `path.org`
  - Notes:
    - Response body references #/components/schemas/org-membership

### PATCH Routes (1)

#### `PATCH /user/memberships/orgs/{org}`
**Summary:** Update an organization membership for the authenticated user
**Status:** planned

**Operations:**
- **update_partial**
  - Component: `org-membership`
  - Filters:
    - `org` eq `path.org`
  - Notes:
    - Response body references #/components/schemas/org-membership

### PUT Routes (1)

#### `PUT /orgs/{org}/memberships/{username}`
**Summary:** Set organization membership for a user
**Status:** planned

**Operations:**
- **update**
  - Component: `org-membership`
  - Filters:
    - `org` eq `path.org`
    - `username` eq `path.username`
  - Notes:
    - Response body references #/components/schemas/org-membership
