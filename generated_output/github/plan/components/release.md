# Component Plan: `release`

**API Slug:** `github`
**Total Routes:** 5

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`update_partial`**: Apply a partial update to a record.

## Routes

### GET Routes (3)

#### `GET /repos/{owner}/{repo}/releases/latest`
**Summary:** Get the latest release
**Status:** planned

**Operations:**
- **read_one**
  - Component: `release`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/release

#### `GET /repos/{owner}/{repo}/releases/tags/{tag}`
**Summary:** Get a release by tag name
**Status:** planned

**Operations:**
- **read_one**
  - Component: `release`
  - Filters:
    - `tag` eq `path.tag`
  - Notes:
    - Response body references #/components/schemas/release
    - Query parameters: tag

#### `GET /repos/{owner}/{repo}/releases/{release_id}`
**Summary:** Get a release
**Status:** planned

**Operations:**
- **read_one**
  - Component: `release`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `release_id` eq `path.release_id`
  - Notes:
    - Response body references #/components/schemas/release

### PATCH Routes (1)

#### `PATCH /repos/{owner}/{repo}/releases/{release_id}`
**Summary:** Update a release
**Status:** planned

**Operations:**
- **update_partial**
  - Component: `release`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `release_id` eq `path.release_id`
  - Notes:
    - Response body references #/components/schemas/release

### POST Routes (1)

#### `POST /repos/{owner}/{repo}/releases`
**Summary:** Create a release
**Status:** planned

**Operations:**
- **create**
  - Component: `release`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/release
