# Component Plan: `pull-request-review-request`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/pulls/{pull_number}/requested_reviewers`
**Summary:** Get all requested reviewers for a pull request
**Status:** planned

**Operations:**
- **read_one**
  - Component: `pull-request-review-request`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `pull_number` eq `path.pull_number`
  - Notes:
    - Response body references #/components/schemas/pull-request-review-request
