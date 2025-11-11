# Component Plan: `file-commit`

**API Slug:** `github`
**Total Routes:** 2

## Supported Operations
- **`update`**: Replace a full record.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (1)

#### `DELETE /repos/{owner}/{repo}/contents/{path}`
**Summary:** Delete a file
**Status:** planned

**Operations:**
- **delete**
  - Component: `file-commit`
  - Filters:
    - `path` eq `path.path`
  - Notes:
    - Response body references #/components/schemas/file-commit
    - Query parameters: path

### PUT Routes (1)

#### `PUT /repos/{owner}/{repo}/contents/{path}`
**Summary:** Create or update file contents
**Status:** planned

**Operations:**
- **update**
  - Component: `file-commit`
  - Filters:
    - `path` eq `path.path`
  - Notes:
    - Response body references #/components/schemas/file-commit
    - Query parameters: path
