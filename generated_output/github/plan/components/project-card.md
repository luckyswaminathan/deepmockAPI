# Component Plan: `project-card`

**API Slug:** `github`
**Total Routes:** 3

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`update_partial`**: Apply a partial update to a record.

## Routes

### GET Routes (1)

#### `GET /projects/columns/cards/{card_id}`
**Summary:** Get a project card
**Status:** planned

**Operations:**
- **read_one**
  - Component: `project-card`
  - Filters:
    - `card_id` eq `path.card_id`
  - Notes:
    - Response body references #/components/schemas/project-card

### PATCH Routes (1)

#### `PATCH /projects/columns/cards/{card_id}`
**Summary:** Update an existing project card
**Status:** planned

**Operations:**
- **update_partial**
  - Component: `project-card`
  - Filters:
    - `card_id` eq `path.card_id`
  - Notes:
    - Response body references #/components/schemas/project-card

### POST Routes (1)

#### `POST /projects/columns/{column_id}/cards`
**Summary:** Create a project card
**Status:** planned

**Operations:**
- **create**
  - Component: `project-card`
  - Filters:
    - `column_id` eq `path.column_id`
  - Notes:
    - Response body references #/components/schemas/project-card
