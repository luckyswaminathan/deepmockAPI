# Component Plan: `file_link`

**API Slug:** `stripe`
**Total Routes:** 4

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.

## Routes

### GET Routes (2)

#### `GET /v1/file_links`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `file_link`
  - Notes:
    - Query parameters: created, ending_before, expand, expired, file, limit, starting_after

#### `GET /v1/file_links/{link}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `file_link`
  - Filters:
    - `link` eq `path.link`
  - Notes:
    - Response body references #/components/schemas/file_link
    - Query parameters: expand

### POST Routes (2)

#### `POST /v1/file_links`
**Status:** planned

**Operations:**
- **create**
  - Component: `file_link`
  - Notes:
    - Response body references #/components/schemas/file_link

#### `POST /v1/file_links/{link}`
**Status:** planned

**Operations:**
- **create**
  - Component: `file_link`
  - Filters:
    - `link` eq `path.link`
  - Notes:
    - Response body references #/components/schemas/file_link
    - Query parameters: link
