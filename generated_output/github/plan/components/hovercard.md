# Component Plan: `hovercard`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /users/{username}/hovercard`
**Summary:** Get contextual information for a user
**Status:** planned

**Operations:**
- **read_one**
  - Component: `hovercard`
  - Filters:
    - `username` eq `path.username`
  - Notes:
    - Response body references #/components/schemas/hovercard
    - Query parameters: subject_type, subject_id
