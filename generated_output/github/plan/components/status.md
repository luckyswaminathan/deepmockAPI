# Component Plan: `status`

**API Slug:** `github`
**Total Routes:** 3

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (2)

#### `GET /repos/{owner}/{repo}/commits/{ref}/statuses`
**Summary:** List commit statuses for a reference
**Status:** planned

**Operations:**
- **read_one**
  - Component: `status`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `ref` eq `path.ref`

#### `GET /repos/{owner}/{repo}/deployments/{deployment_id}/statuses`
**Summary:** List deployment statuses
**Status:** planned

**Operations:**
- **read_one**
  - Component: `status`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `deployment_id` eq `path.deployment_id`

### POST Routes (1)

#### `POST /repos/{owner}/{repo}/statuses/{sha}`
**Summary:** Create a commit status
**Status:** planned

**Operations:**
- **create**
  - Component: `status`
  - Filters:
    - `sha` eq `path.sha`
  - Notes:
    - Response body references #/components/schemas/status
    - Query parameters: sha
