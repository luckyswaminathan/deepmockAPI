# Component Plan: `deployment-branch-policy`

**API Slug:** `github`
**Total Routes:** 3

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (1)

#### `DELETE /repos/{owner}/{repo}/environments/{environment_name}/deployment-branch-policies/{branch_policy_id}`
**Summary:** Delete a deployment branch policy
**Status:** planned

**Operations:**
- **delete**
  - Component: `deployment-branch-policy`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `environment_name` eq `path.environment_name`
    - `branch_policy_id` eq `path.branch_policy_id`

### GET Routes (2)

#### `GET /repos/{owner}/{repo}/environments/{environment_name}/deployment-branch-policies`
**Summary:** List deployment branch policies
**Status:** planned

**Operations:**
- **read_one**
  - Component: `deployment-branch-policy`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `environment_name` eq `path.environment_name`

#### `GET /repos/{owner}/{repo}/environments/{environment_name}/deployment-branch-policies/{branch_policy_id}`
**Summary:** Get a deployment branch policy
**Status:** planned

**Operations:**
- **read_one**
  - Component: `deployment-branch-policy`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `environment_name` eq `path.environment_name`
    - `branch_policy_id` eq `path.branch_policy_id`
  - Notes:
    - Response body references #/components/schemas/deployment-branch-policy
