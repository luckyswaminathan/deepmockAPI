# Component Plan: `base-gist`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`create`**: Create a new record for the component.

## Routes

### POST Routes (1)

#### `POST /gists/{gist_id}/forks`
**Summary:** Fork a gist
**Status:** planned

**Operations:**
- **create**
  - Component: `base-gist`
  - Filters:
    - `gist_id` eq `path.gist_id`
  - Notes:
    - Response body references #/components/schemas/base-gist
