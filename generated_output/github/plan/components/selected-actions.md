# Component Plan: `selected-actions`

**API Slug:** `github`
**Total Routes:** 4

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.
- **`update`**: Replace a full record.

## Routes

### GET Routes (2)

#### `GET /orgs/{org}/actions/permissions/selected-actions`
**Summary:** Get allowed actions and reusable workflows for an organization
**Status:** planned

**Operations:**
- **read_one**
  - Component: `selected-actions`
  - Filters:
    - `org` eq `path.org`
  - Notes:
    - Response body references #/components/schemas/selected-actions

#### `GET /repos/{owner}/{repo}/actions/permissions/selected-actions`
**Summary:** Get allowed actions and reusable workflows for a repository
**Status:** planned

**Operations:**
- **read_one**
  - Component: `selected-actions`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/selected-actions

### PUT Routes (2)

#### `PUT /orgs/{org}/actions/permissions/selected-actions`
**Summary:** Set allowed actions and reusable workflows for an organization
**Status:** planned

**Operations:**
- **update**
  - Component: `selected-actions`
  - Filters:
    - `org` eq `path.org`
  - Notes:
    - Request body references #/components/schemas/selected-actions

#### `PUT /repos/{owner}/{repo}/actions/permissions/selected-actions`
**Summary:** Set allowed actions and reusable workflows for a repository
**Status:** planned

**Operations:**
- **update**
  - Component: `selected-actions`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Request body references #/components/schemas/selected-actions
