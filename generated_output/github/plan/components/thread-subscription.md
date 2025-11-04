# Component Plan: `thread-subscription`

**API Slug:** `github`
**Total Routes:** 2

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.
- **`update`**: Replace a full record.

## Routes

### GET Routes (1)

#### `GET /notifications/threads/{thread_id}/subscription`
**Summary:** Get a thread subscription for the authenticated user
**Status:** planned

**Operations:**
- **read_one**
  - Component: `thread-subscription`
  - Filters:
    - `thread_id` eq `path.thread_id`
  - Notes:
    - Response body references #/components/schemas/thread-subscription

### PUT Routes (1)

#### `PUT /notifications/threads/{thread_id}/subscription`
**Summary:** Set a thread subscription
**Status:** planned

**Operations:**
- **update**
  - Component: `thread-subscription`
  - Filters:
    - `thread_id` eq `path.thread_id`
  - Notes:
    - Response body references #/components/schemas/thread-subscription
