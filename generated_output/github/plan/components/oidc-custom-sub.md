# Component Plan: `oidc-custom-sub`

**API Slug:** `github`
**Total Routes:** 2

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.
- **`update`**: Replace a full record.

## Routes

### GET Routes (1)

#### `GET /orgs/{org}/actions/oidc/customization/sub`
**Summary:** Get the customization template for an OIDC subject claim for an organization
**Status:** planned

**Operations:**
- **read_one**
  - Component: `oidc-custom-sub`
  - Filters:
    - `org` eq `path.org`
  - Notes:
    - Response body references #/components/schemas/oidc-custom-sub

### PUT Routes (1)

#### `PUT /orgs/{org}/actions/oidc/customization/sub`
**Summary:** Set the customization template for an OIDC subject claim for an organization
**Status:** planned

**Operations:**
- **update**
  - Component: `oidc-custom-sub`
  - Filters:
    - `org` eq `path.org`
  - Notes:
    - Request body references #/components/schemas/oidc-custom-sub
    - Response body references #/components/schemas/empty-object
