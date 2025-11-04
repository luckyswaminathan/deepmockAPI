# Component Plan: `thread`

**API Slug:** `github`
**Total Routes:** 3

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.
- **`update_partial`**: Apply a partial update to a record.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (1)

#### `DELETE /notifications/threads/{thread_id}`
**Summary:** Mark a thread as done
**Status:** planned

**Operations:**
- **delete**
  - Component: `thread`
  - Filters:
    - `thread_id` eq `path.thread_id`

### GET Routes (1)

#### `GET /notifications/threads/{thread_id}`
**Summary:** Get a thread
**Status:** planned

**Operations:**
- **read_one**
  - Component: `thread`
  - Filters:
    - `thread_id` eq `path.thread_id`
  - Notes:
    - Response body references #/components/schemas/thread

### PATCH Routes (1)

#### `PATCH /notifications/threads/{thread_id}`
**Summary:** Mark a thread as read
**Status:** planned

**Operations:**
- **update_partial**
  - Component: `thread`
  - Filters:
    - `thread_id` eq `path.thread_id`
