# Component Plan: `release-asset`

**API Slug:** `github`
**Total Routes:** 3

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`update_partial`**: Apply a partial update to a record.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/releases/assets/{asset_id}`
**Summary:** Get a release asset
**Status:** planned

**Operations:**
- **read_one**
  - Component: `release-asset`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `asset_id` eq `path.asset_id`
  - Notes:
    - Response body references #/components/schemas/release-asset

### PATCH Routes (1)

#### `PATCH /repos/{owner}/{repo}/releases/assets/{asset_id}`
**Summary:** Update a release asset
**Status:** planned

**Operations:**
- **update_partial**
  - Component: `release-asset`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `asset_id` eq `path.asset_id`
  - Notes:
    - Response body references #/components/schemas/release-asset

### POST Routes (1)

#### `POST /repos/{owner}/{repo}/releases/{release_id}/assets`
**Summary:** Upload a release asset
**Status:** planned

**Operations:**
- **create**
  - Component: `release-asset`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `release_id` eq `path.release_id`
  - Notes:
    - Response body references #/components/schemas/release-asset
    - Query parameters: name, label
