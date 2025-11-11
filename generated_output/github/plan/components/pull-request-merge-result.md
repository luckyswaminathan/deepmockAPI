# Component Plan: `pull-request-merge-result`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`update`**: Replace a full record.

## Routes

### PUT Routes (1)

#### `PUT /repos/{owner}/{repo}/pulls/{pull_number}/merge`
**Summary:** Merge a pull request
**Status:** planned

**Operations:**
- **update**
  - Component: `pull-request-merge-result`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `pull_number` eq `path.pull_number`
  - Notes:
    - Response body references #/components/schemas/pull-request-merge-result
