# Component Plan: `pull-request-simple`

**API Slug:** `github`
**Total Routes:** 2

## Supported Operations
- **`create`**: Create a new record for the component.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (1)

#### `DELETE /repos/{owner}/{repo}/pulls/{pull_number}/requested_reviewers`
**Summary:** Remove requested reviewers from a pull request
**Status:** planned

**Operations:**
- **delete**
  - Component: `pull-request-simple`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `pull_number` eq `path.pull_number`
  - Notes:
    - Response body references #/components/schemas/pull-request-simple

### POST Routes (1)

#### `POST /repos/{owner}/{repo}/pulls/{pull_number}/requested_reviewers`
**Summary:** Request reviewers for a pull request
**Status:** planned

**Operations:**
- **create**
  - Component: `pull-request-simple`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `pull_number` eq `path.pull_number`
  - Notes:
    - Response body references #/components/schemas/pull-request-simple
