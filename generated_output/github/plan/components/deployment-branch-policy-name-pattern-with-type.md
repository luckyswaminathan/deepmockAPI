# Component Plan: `deployment-branch-policy-name-pattern-with-type`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`create`**: Create a new record for the component.

## Routes

### POST Routes (1)

#### `POST /repos/{owner}/{repo}/environments/{environment_name}/deployment-branch-policies`
**Summary:** Create a deployment branch policy
**Status:** planned

**Operations:**
- **create**
  - Component: `deployment-branch-policy-name-pattern-with-type`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `environment_name` eq `path.environment_name`
  - Notes:
    - Request body references #/components/schemas/deployment-branch-policy-name-pattern-with-type
    - Response body references #/components/schemas/deployment-branch-policy
