# Component Plan: `minimal-repository`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`create`**: Create a new record for the component.

## Routes

### POST Routes (1)

#### `POST /repos/{owner}/{repo}/transfer`
**Summary:** Transfer a repository
**Status:** planned

**Operations:**
- **create**
  - Component: `minimal-repository`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/minimal-repository
