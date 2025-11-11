# Component Plan: `actions-get-default-workflow-permissions`

**API Slug:** `github`
**Total Routes:** 2

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (2)

#### `GET /orgs/{org}/actions/permissions/workflow`
**Summary:** Get default workflow permissions for an organization
**Status:** planned

**Operations:**
- **read_one**
  - Component: `actions-get-default-workflow-permissions`
  - Filters:
    - `org` eq `path.org`
  - Notes:
    - Response body references #/components/schemas/actions-get-default-workflow-permissions

#### `GET /repos/{owner}/{repo}/actions/permissions/workflow`
**Summary:** Get default workflow permissions for a repository
**Status:** planned

**Operations:**
- **read_one**
  - Component: `actions-get-default-workflow-permissions`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/actions-get-default-workflow-permissions
