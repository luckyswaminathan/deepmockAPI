# Component Plan: `workflow-run`

**API Slug:** `github`
**Total Routes:** 2

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (2)

#### `GET /repos/{owner}/{repo}/actions/runs/{run_id}`
**Summary:** Get a workflow run
**Status:** planned

**Operations:**
- **read_one**
  - Component: `workflow-run`
  - Filters:
    - `owner` eq `path.owner`
    - `repository` eq `path.repo`
    - `run_id` eq `path.run_id`
  - Notes:
    - Response body references #/components/schemas/workflow-run

#### `GET /repos/{owner}/{repo}/actions/runs/{run_id}/attempts/{attempt_number}`
**Summary:** Get a workflow run attempt
**Status:** planned

**Operations:**
- **read_one**
  - Component: `workflow-run`
  - Filters:
    - `owner` eq `path.owner`
    - `repository` eq `path.repo`
    - `run_id` eq `path.run_id`
    - `attempt_number` eq `path.attempt_number`
  - Notes:
    - Response body references #/components/schemas/workflow-run
