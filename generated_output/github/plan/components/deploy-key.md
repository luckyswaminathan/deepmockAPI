# Component Plan: `deploy-key`

**API Slug:** `github`
**Total Routes:** 2

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/keys/{key_id}`
**Summary:** Get a deploy key
**Status:** planned

**Operations:**
- **read_one**
  - Component: `deploy-key`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `key_id` eq `path.key_id`
  - Notes:
    - Response body references #/components/schemas/deploy-key

### POST Routes (1)

#### `POST /repos/{owner}/{repo}/keys`
**Summary:** Create a deploy key
**Status:** planned

**Operations:**
- **create**
  - Component: `deploy-key`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/deploy-key
