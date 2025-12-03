# Component Plan: `merge-group`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/pulls/{pull_number}/merge`
**Summary:** Check if a pull request has been merged
**Status:** planned

**Operations:**
- **read_one**
  - Component: `merge-group`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `pull_number` eq `path.pull_number`
