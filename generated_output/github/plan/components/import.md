# Component Plan: `import`

**API Slug:** `github`
**Total Routes:** 5

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.
- **`update`**: Replace a full record.
- **`update_partial`**: Apply a partial update to a record.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (1)

#### `DELETE /repos/{owner}/{repo}/import`
**Summary:** Cancel an import
**Status:** planned

**Operations:**
- **delete**
  - Component: `import`
  - Filters:
    - `owner` eq `path.owner`
    - `repository_url` eq `path.repo`

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/import`
**Summary:** Get an import status
**Status:** planned

**Operations:**
- **read_one**
  - Component: `import`
  - Filters:
    - `owner` eq `path.owner`
    - `repository_url` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/import

### PATCH Routes (2)

#### `PATCH /repos/{owner}/{repo}/import`
**Summary:** Update an import
**Status:** planned

**Operations:**
- **update_partial**
  - Component: `import`
  - Filters:
    - `owner` eq `path.owner`
    - `repository_url` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/import

#### `PATCH /repos/{owner}/{repo}/import/lfs`
**Summary:** Update Git LFS preference
**Status:** planned

**Operations:**
- **update_partial**
  - Component: `import`
  - Filters:
    - `owner` eq `path.owner`
    - `repository_url` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/import

### PUT Routes (1)

#### `PUT /repos/{owner}/{repo}/import`
**Summary:** Start an import
**Status:** planned

**Operations:**
- **update**
  - Component: `import`
  - Filters:
    - `owner` eq `path.owner`
    - `repository_url` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/import
