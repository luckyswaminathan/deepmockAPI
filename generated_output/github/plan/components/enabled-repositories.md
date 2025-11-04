# Component Plan: `enabled-repositories`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`update`**: Replace a full record.

## Routes

### PUT Routes (1)

#### `PUT /repos/{owner}/{repo}/actions/workflows/{workflow_id}/enable`
**Summary:** Enable a workflow
**Status:** planned

**Operations:**
- **update**
  - Component: `enabled-repositories`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `workflow_id` eq `path.workflow_id`
