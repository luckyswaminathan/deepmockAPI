# Component Plan: `gist-simple`

**API Slug:** `github`
**Total Routes:** 4

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`update_partial`**: Apply a partial update to a record.

## Routes

### GET Routes (2)

#### `GET /gists/{gist_id}`
**Summary:** Get a gist
**Status:** planned

**Operations:**
- **read_one**
  - Component: `gist-simple`
  - Filters:
    - `gist_id` eq `path.gist_id`
  - Notes:
    - Response body references #/components/schemas/gist-simple

#### `GET /gists/{gist_id}/{sha}`
**Summary:** Get a gist revision
**Status:** planned

**Operations:**
- **read_one**
  - Component: `gist-simple`
  - Filters:
    - `sha` eq `path.sha`
  - Notes:
    - Response body references #/components/schemas/gist-simple
    - Query parameters: sha

### PATCH Routes (1)

#### `PATCH /gists/{gist_id}`
**Summary:** Update a gist
**Status:** planned

**Operations:**
- **update_partial**
  - Component: `gist-simple`
  - Filters:
    - `gist_id` eq `path.gist_id`
  - Notes:
    - Response body references #/components/schemas/gist-simple

### POST Routes (1)

#### `POST /gists`
**Summary:** Create a gist
**Status:** planned

**Operations:**
- **create**
  - Component: `gist-simple`
  - Notes:
    - Response body references #/components/schemas/gist-simple
