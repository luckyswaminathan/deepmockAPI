# Component Plan: `page-build-status`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`create`**: Create a new record for the component.

## Routes

### POST Routes (1)

#### `POST /repos/{owner}/{repo}/pages/builds`
**Summary:** Request a GitHub Pages build
**Status:** planned

**Operations:**
- **create**
  - Component: `page-build-status`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/page-build-status
