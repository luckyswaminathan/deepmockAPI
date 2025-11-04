# Component Plan: `issue-comment`

**API Slug:** `github`
**Total Routes:** 3

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`update_partial`**: Apply a partial update to a record.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/issues/comments/{comment_id}`
**Summary:** Get an issue comment
**Status:** planned

**Operations:**
- **read_one**
  - Component: `issue-comment`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `comment_id` eq `path.comment_id`
  - Notes:
    - Response body references #/components/schemas/issue-comment

### PATCH Routes (1)

#### `PATCH /repos/{owner}/{repo}/issues/comments/{comment_id}`
**Summary:** Update an issue comment
**Status:** planned

**Operations:**
- **update_partial**
  - Component: `issue-comment`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `comment_id` eq `path.comment_id`
  - Notes:
    - Response body references #/components/schemas/issue-comment

### POST Routes (1)

#### `POST /repos/{owner}/{repo}/issues/{issue_number}/comments`
**Summary:** Create an issue comment
**Status:** planned

**Operations:**
- **create**
  - Component: `issue-comment`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `issue_number` eq `path.issue_number`
  - Notes:
    - Response body references #/components/schemas/issue-comment
