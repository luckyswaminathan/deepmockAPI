# Component Plan: `issue-event`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/issues/events/{event_id}`
**Summary:** Get an issue event
**Status:** planned

**Operations:**
- **read_one**
  - Component: `issue-event`
  - Filters:
    - `event_id` eq `path.event_id`
  - Notes:
    - Response body references #/components/schemas/issue-event
    - Query parameters: event_id
