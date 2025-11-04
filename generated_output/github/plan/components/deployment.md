# Component Plan: `deployment`

**API Slug:** `github`
**Total Routes:** 4

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (1)

#### `DELETE /repos/{owner}/{repo}/deployments/{deployment_id}`
**Summary:** Delete a deployment
**Status:** planned

**Operations:**
- **delete**
  - Component: `deployment`
  - Filters:
    - `owner` eq `path.owner`
    - `repository_url` eq `path.repo`
    - `deployment_id` eq `path.deployment_id`

### GET Routes (2)

#### `GET /repos/{owner}/{repo}/deployments`
**Summary:** List deployments
**Status:** planned

**Operations:**
- **read_one**
  - Component: `deployment`
  - Filters:
    - `owner` eq `path.owner`
    - `repository_url` eq `path.repo`
  - Notes:
    - Query parameters: sha, ref, task, environment

#### `GET /repos/{owner}/{repo}/deployments/{deployment_id}`
**Summary:** Get a deployment
**Status:** planned

**Operations:**
- **read_one**
  - Component: `deployment`
  - Filters:
    - `owner` eq `path.owner`
    - `repository_url` eq `path.repo`
    - `deployment_id` eq `path.deployment_id`
  - Notes:
    - Response body references #/components/schemas/deployment

### POST Routes (1)

#### `POST /repos/{owner}/{repo}/deployments`
**Summary:** Create a deployment
**Status:** planned

**Operations:**
- **create**
  - Component: `deployment`
  - Filters:
    - `owner` eq `path.owner`
    - `repository_url` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/deployment
