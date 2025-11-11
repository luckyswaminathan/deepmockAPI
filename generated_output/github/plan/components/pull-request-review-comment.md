# Component Plan: `pull-request-review-comment`

**API Slug:** `github`
**Total Routes:** 4

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`update_partial`**: Apply a partial update to a record.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/pulls/comments/{comment_id}`
**Summary:** Get a review comment for a pull request
**Status:** planned

**Operations:**
- **read_one**
  - Component: `pull-request-review-comment`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `comment_id` eq `path.comment_id`
  - Notes:
    - Response body references #/components/schemas/pull-request-review-comment

### PATCH Routes (1)

#### `PATCH /repos/{owner}/{repo}/pulls/comments/{comment_id}`
**Summary:** Update a review comment for a pull request
**Status:** planned

**Operations:**
- **update_partial**
  - Component: `pull-request-review-comment`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `comment_id` eq `path.comment_id`
  - Notes:
    - Response body references #/components/schemas/pull-request-review-comment

### POST Routes (2)

#### `POST /repos/{owner}/{repo}/pulls/{pull_number}/comments`
**Summary:** Create a review comment for a pull request
**Status:** planned

**Operations:**
- **create**
  - Component: `pull-request-review-comment`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `pull_number` eq `path.pull_number`
  - Notes:
    - Response body references #/components/schemas/pull-request-review-comment

#### `POST /repos/{owner}/{repo}/pulls/{pull_number}/comments/{comment_id}/replies`
**Summary:** Create a reply for a review comment
**Status:** planned

**Operations:**
- **create**
  - Component: `pull-request-review-comment`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `pull_number` eq `path.pull_number`
    - `comment_id` eq `path.comment_id`
  - Notes:
    - Response body references #/components/schemas/pull-request-review-comment
