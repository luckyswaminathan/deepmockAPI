# Component Plan: `merged-upstream`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`create`**: Create a new record for the component.

## Routes

### POST Routes (1)

#### `POST /repos/{owner}/{repo}/merge-upstream`
**Summary:** Sync a fork branch with the upstream repository
**Status:** planned

**Operations:**
- **create**
  - Component: `merged-upstream`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/merged-upstream
