# Component Plan: `codespace-export-details`

**API Slug:** `github`
**Total Routes:** 2

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /user/codespaces/{codespace_name}/exports/{export_id}`
**Summary:** Get details about a codespace export
**Status:** planned

**Operations:**
- **read_one**
  - Component: `codespace-export-details`
  - Filters:
    - `codespace_name` eq `path.codespace_name`
    - `export_id` eq `path.export_id`
  - Notes:
    - Response body references #/components/schemas/codespace-export-details

### POST Routes (1)

#### `POST /user/codespaces/{codespace_name}/exports`
**Summary:** Export a codespace for the authenticated user
**Status:** planned

**Operations:**
- **create**
  - Component: `codespace-export-details`
  - Filters:
    - `codespace_name` eq `path.codespace_name`
  - Notes:
    - Response body references #/components/schemas/codespace-export-details
