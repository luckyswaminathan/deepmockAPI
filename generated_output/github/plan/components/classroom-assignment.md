# Component Plan: `classroom-assignment`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /assignments/{assignment_id}`
**Summary:** Get an assignment
**Status:** planned

**Operations:**
- **read_one**
  - Component: `classroom-assignment`
  - Filters:
    - `assignment_id` eq `path.assignment_id`
  - Notes:
    - Response body references #/components/schemas/classroom-assignment
