# Component Plan: `actions-set-default-workflow-permissions`

**API Slug:** `github`
**Total Routes:** 2

## Supported Operations
- **`update`**: Replace a full record.

## Routes

### PUT Routes (2)

#### `PUT /orgs/{org}/actions/permissions/workflow`
**Summary:** Set default workflow permissions for an organization
**Status:** planned

**Operations:**
- **update**
  - Component: `actions-set-default-workflow-permissions`
  - Filters:
    - `org` eq `path.org`
  - Notes:
    - Request body references #/components/schemas/actions-set-default-workflow-permissions

#### `PUT /repos/{owner}/{repo}/actions/permissions/workflow`
**Summary:** Set default workflow permissions for a repository
**Status:** planned

**Operations:**
- **update**
  - Component: `actions-set-default-workflow-permissions`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Request body references #/components/schemas/actions-set-default-workflow-permissions
