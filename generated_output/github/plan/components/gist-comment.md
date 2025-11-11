# Component Plan: `gist-comment`

**API Slug:** `github`
**Total Routes:** 3

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`update_partial`**: Apply a partial update to a record.

## Routes

### GET Routes (1)

#### `GET /gists/{gist_id}/comments/{comment_id}`
**Summary:** Get a gist comment
**Status:** planned

**Operations:**
- **read_one**
  - Component: `gist-comment`
  - Filters:
    - `gist_id` eq `path.gist_id`
    - `comment_id` eq `path.comment_id`
  - Notes:
    - Response body references #/components/schemas/gist-comment

### PATCH Routes (1)

#### `PATCH /gists/{gist_id}/comments/{comment_id}`
**Summary:** Update a gist comment
**Status:** planned

**Operations:**
- **update_partial**
  - Component: `gist-comment`
  - Filters:
    - `gist_id` eq `path.gist_id`
    - `comment_id` eq `path.comment_id`
  - Notes:
    - Response body references #/components/schemas/gist-comment

### POST Routes (1)

#### `POST /gists/{gist_id}/comments`
**Summary:** Create a gist comment
**Status:** planned

**Operations:**
- **create**
  - Component: `gist-comment`
  - Filters:
    - `gist_id` eq `path.gist_id`
  - Notes:
    - Response body references #/components/schemas/gist-comment
