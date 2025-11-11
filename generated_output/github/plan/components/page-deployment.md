# Component Plan: `page-deployment`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`create`**: Create a new record for the component.

## Routes

### POST Routes (1)

#### `POST /repos/{owner}/{repo}/pages/deployments`
**Summary:** Create a GitHub Pages deployment
**Status:** planned

**Operations:**
- **create**
  - Component: `page-deployment`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/page-deployment
