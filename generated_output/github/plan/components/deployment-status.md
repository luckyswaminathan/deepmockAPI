# Component Plan: `deployment-status`

**API Slug:** `github`
**Total Routes:** 2

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/deployments/{deployment_id}/statuses/{status_id}`
**Summary:** Get a deployment status
**Status:** planned

**Operations:**
- **read_one**
  - Component: `deployment-status`
  - Filters:
    - `status_id` eq `path.status_id`
  - Notes:
    - Response body references #/components/schemas/deployment-status
    - Query parameters: status_id

### POST Routes (1)

#### `POST /repos/{owner}/{repo}/deployments/{deployment_id}/statuses`
**Summary:** Create a deployment status
**Status:** planned

**Operations:**
- **create**
  - Component: `deployment-status`
  - Filters:
    - `owner` eq `path.owner`
    - `repository_url` eq `path.repo`
    - `deployment_id` eq `path.deployment_id`
  - Notes:
    - Response body references #/components/schemas/deployment-status
