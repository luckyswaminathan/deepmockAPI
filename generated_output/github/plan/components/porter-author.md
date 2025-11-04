# Component Plan: `porter-author`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`update_partial`**: Apply a partial update to a record.

## Routes

### PATCH Routes (1)

#### `PATCH /repos/{owner}/{repo}/import/authors/{author_id}`
**Summary:** Map a commit author
**Status:** planned

**Operations:**
- **update_partial**
  - Component: `porter-author`
  - Filters:
    - `author_id` eq `path.author_id`
  - Notes:
    - Response body references #/components/schemas/porter-author
    - Query parameters: author_id
