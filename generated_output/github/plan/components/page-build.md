# Component Plan: `page-build`

**API Slug:** `github`
**Total Routes:** 2

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (2)

#### `GET /repos/{owner}/{repo}/pages/builds/latest`
**Summary:** Get latest Pages build
**Status:** planned

**Operations:**
- **read_one**
  - Component: `page-build`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/page-build

#### `GET /repos/{owner}/{repo}/pages/builds/{build_id}`
**Summary:** Get GitHub Pages build
**Status:** planned

**Operations:**
- **read_one**
  - Component: `page-build`
  - Filters:
    - `build_id` eq `path.build_id`
  - Notes:
    - Response body references #/components/schemas/page-build
    - Query parameters: build_id
