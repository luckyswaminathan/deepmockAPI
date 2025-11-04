# Component Plan: `content-file`

**API Slug:** `github`
**Total Routes:** 2

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (2)

#### `GET /repos/{owner}/{repo}/readme`
**Summary:** Get a repository README
**Status:** planned

**Operations:**
- **read_one**
  - Component: `content-file`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/content-file
    - Query parameters: ref

#### `GET /repos/{owner}/{repo}/readme/{dir}`
**Summary:** Get a repository README for a directory
**Status:** planned

**Operations:**
- **read_one**
  - Component: `content-file`
  - Filters:
    - `dir` eq `path.dir`
  - Notes:
    - Response body references #/components/schemas/content-file
    - Query parameters: ref
