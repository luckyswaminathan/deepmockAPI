# Component Plan: `merged-upstream`

**API Slug:** `github`
**Total Routes:** 2

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/pulls/{pull_number}/merge`
**Summary:** Check if a pull request has been merged
**Status:** planned

**Operations:**
- **read_one**
  - Component: `merged-upstream`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `pull_number` eq `path.pull_number`

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
