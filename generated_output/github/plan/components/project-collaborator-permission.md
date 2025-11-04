# Component Plan: `project-collaborator-permission`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /projects/{project_id}/collaborators/{username}/permission`
**Summary:** Get project permission for a user
**Status:** planned

**Operations:**
- **read_one**
  - Component: `project-collaborator-permission`
  - Filters:
    - `project_id` eq `path.project_id`
    - `username` eq `path.username`
  - Notes:
    - Response body references #/components/schemas/project-collaborator-permission
