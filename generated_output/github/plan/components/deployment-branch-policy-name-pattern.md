# Component Plan: `deployment-branch-policy-name-pattern`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`update`**: Replace a full record.

## Routes

### PUT Routes (1)

#### `PUT /repos/{owner}/{repo}/environments/{environment_name}/deployment-branch-policies/{branch_policy_id}`
**Summary:** Update a deployment branch policy
**Status:** planned

**Operations:**
- **update**
  - Component: `deployment-branch-policy-name-pattern`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `environment_name` eq `path.environment_name`
    - `branch_policy_id` eq `path.branch_policy_id`
  - Notes:
    - Request body references #/components/schemas/deployment-branch-policy-name-pattern
    - Response body references #/components/schemas/deployment-branch-policy
