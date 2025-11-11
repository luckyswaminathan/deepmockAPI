# Component Plan: `artifact`

**API Slug:** `github`
**Total Routes:** 5

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (1)

#### `DELETE /repos/{owner}/{repo}/actions/artifacts/{artifact_id}`
**Summary:** Delete an artifact
**Status:** planned

**Operations:**
- **delete**
  - Component: `artifact`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `artifact_id` eq `path.artifact_id`

### GET Routes (4)

#### `GET /repos/{owner}/{repo}/actions/artifacts`
**Summary:** List artifacts for a repository
**Status:** planned

**Operations:**
- **read_one**
  - Component: `artifact`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`

#### `GET /repos/{owner}/{repo}/actions/artifacts/{artifact_id}`
**Summary:** Get an artifact
**Status:** planned

**Operations:**
- **read_one**
  - Component: `artifact`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `artifact_id` eq `path.artifact_id`
  - Notes:
    - Response body references #/components/schemas/artifact

#### `GET /repos/{owner}/{repo}/actions/artifacts/{artifact_id}/{archive_format}`
**Summary:** Download an artifact
**Status:** planned

**Operations:**
- **read_one**
  - Component: `artifact`
  - Filters:
    - `archive_format` eq `path.archive_format`
  - Notes:
    - Query parameters: archive_format

#### `GET /repos/{owner}/{repo}/actions/runs/{run_id}/artifacts`
**Summary:** List workflow run artifacts
**Status:** planned

**Operations:**
- **read_one**
  - Component: `artifact`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `run_id` eq `path.run_id`
