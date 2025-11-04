# Component Plan: `project-column`

**API Slug:** `github`
**Total Routes:** 3

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`update_partial`**: Apply a partial update to a record.

## Routes

### GET Routes (1)

#### `GET /projects/columns/{column_id}`
**Summary:** Get a project column
**Status:** planned

**Operations:**
- **read_one**
  - Component: `project-column`
  - Filters:
    - `column_id` eq `path.column_id`
  - Notes:
    - Response body references #/components/schemas/project-column

### PATCH Routes (1)

#### `PATCH /projects/columns/{column_id}`
**Summary:** Update an existing project column
**Status:** planned

**Operations:**
- **update_partial**
  - Component: `project-column`
  - Filters:
    - `column_id` eq `path.column_id`
  - Notes:
    - Response body references #/components/schemas/project-column

### POST Routes (1)

#### `POST /projects/{project_id}/columns`
**Summary:** Create a project column
**Status:** planned

**Operations:**
- **create**
  - Component: `project-column`
  - Filters:
    - `project_id` eq `path.project_id`
  - Notes:
    - Response body references #/components/schemas/project-column
