# Component Plan: `page`

**API Slug:** `github`
**Total Routes:** 4

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`update`**: Replace a full record.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (1)

#### `DELETE /repos/{owner}/{repo}/pages`
**Summary:** Delete a GitHub Pages site
**Status:** planned

**Operations:**
- **delete**
  - Component: `page`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/pages`
**Summary:** Get a GitHub Pages site
**Status:** planned

**Operations:**
- **read_one**
  - Component: `page`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/page

### POST Routes (1)

#### `POST /repos/{owner}/{repo}/pages`
**Summary:** Create a GitHub Pages site
**Status:** planned

**Operations:**
- **create**
  - Component: `page`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/page

### PUT Routes (1)

#### `PUT /repos/{owner}/{repo}/pages`
**Summary:** Update information about a GitHub Pages site
**Status:** planned

**Operations:**
- **update**
  - Component: `page`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
