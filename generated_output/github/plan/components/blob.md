# Component Plan: `blob`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/git/blobs/{file_sha}`
**Summary:** Get a blob
**Status:** planned

**Operations:**
- **read_one**
  - Component: `blob`
  - Filters:
    - `file_sha` eq `path.file_sha`
  - Notes:
    - Response body references #/components/schemas/blob
    - Query parameters: file_sha
