# Component Plan: `workflow-run-usage`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/actions/runs/{run_id}/timing`
**Summary:** Get workflow run usage
**Status:** planned

**Operations:**
- **read_one**
  - Component: `workflow-run-usage`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `run_id` eq `path.run_id`
  - Notes:
    - Response body references #/components/schemas/workflow-run-usage
