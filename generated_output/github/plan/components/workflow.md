# Component Plan: `workflow`

**API Slug:** `github`
**Total Routes:** 2

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (2)

#### `GET /repos/{owner}/{repo}/actions/workflows`
**Summary:** List repository workflows
**Status:** planned

**Operations:**
- **read_one**
  - Component: `workflow`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`

#### `GET /repos/{owner}/{repo}/actions/workflows/{workflow_id}`
**Summary:** Get a workflow
**Status:** planned

**Operations:**
- **read_one**
  - Component: `workflow`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `workflow_id` eq `path.workflow_id`
  - Notes:
    - Response body references #/components/schemas/workflow
