# Component Plan: `commit-comment`

**API Slug:** `github`
**Total Routes:** 3

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`update_partial`**: Apply a partial update to a record.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/comments/{comment_id}`
**Summary:** Get a commit comment
**Status:** planned

**Operations:**
- **read_one**
  - Component: `commit-comment`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `comment_id` eq `path.comment_id`
  - Notes:
    - Response body references #/components/schemas/commit-comment

### PATCH Routes (1)

#### `PATCH /repos/{owner}/{repo}/comments/{comment_id}`
**Summary:** Update a commit comment
**Status:** planned

**Operations:**
- **update_partial**
  - Component: `commit-comment`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `comment_id` eq `path.comment_id`
  - Notes:
    - Response body references #/components/schemas/commit-comment

### POST Routes (1)

#### `POST /repos/{owner}/{repo}/commits/{commit_sha}/comments`
**Summary:** Create a commit comment
**Status:** planned

**Operations:**
- **create**
  - Component: `commit-comment`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `commit_sha` eq `path.commit_sha`
  - Notes:
    - Response body references #/components/schemas/commit-comment
