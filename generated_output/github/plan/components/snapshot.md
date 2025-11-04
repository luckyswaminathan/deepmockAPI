# Component Plan: `snapshot`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`create`**: Create a new record for the component.

## Routes

### POST Routes (1)

#### `POST /repos/{owner}/{repo}/dependency-graph/snapshots`
**Summary:** Create a snapshot of dependencies for a repository
**Status:** planned

**Operations:**
- **create**
  - Component: `snapshot`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Request body references #/components/schemas/snapshot
