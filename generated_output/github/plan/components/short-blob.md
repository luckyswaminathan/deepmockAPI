# Component Plan: `short-blob`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`create`**: Create a new record for the component.

## Routes

### POST Routes (1)

#### `POST /repos/{owner}/{repo}/git/blobs`
**Summary:** Create a blob
**Status:** planned

**Operations:**
- **create**
  - Component: `short-blob`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/short-blob
