# Component Plan: `pages-deployment-status`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/pages/deployments/{pages_deployment_id}`
**Summary:** Get the status of a GitHub Pages deployment
**Status:** planned

**Operations:**
- **read_one**
  - Component: `pages-deployment-status`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `pages_deployment_id` eq `path.pages_deployment_id`
  - Notes:
    - Response body references #/components/schemas/pages-deployment-status
