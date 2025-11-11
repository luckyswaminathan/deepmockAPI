# Component Plan: `workflow-usage`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/actions/workflows/{workflow_id}/timing`
**Summary:** Get workflow usage
**Status:** planned

**Operations:**
- **read_one**
  - Component: `workflow-usage`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `workflow_id` eq `path.workflow_id`
  - Notes:
    - Response body references #/components/schemas/workflow-usage
