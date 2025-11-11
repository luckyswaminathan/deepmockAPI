# Component Plan: `environment`

**API Slug:** `github`
**Total Routes:** 4

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.
- **`update`**: Replace a full record.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (1)

#### `DELETE /repos/{owner}/{repo}/environments/{environment_name}`
**Summary:** Delete an environment
**Status:** planned

**Operations:**
- **delete**
  - Component: `environment`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `environment_name` eq `path.environment_name`

### GET Routes (2)

#### `GET /repos/{owner}/{repo}/environments`
**Summary:** List environments
**Status:** planned

**Operations:**
- **read_one**
  - Component: `environment`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`

#### `GET /repos/{owner}/{repo}/environments/{environment_name}`
**Summary:** Get an environment
**Status:** planned

**Operations:**
- **read_one**
  - Component: `environment`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `environment_name` eq `path.environment_name`
  - Notes:
    - Response body references #/components/schemas/environment

### PUT Routes (1)

#### `PUT /repos/{owner}/{repo}/environments/{environment_name}`
**Summary:** Create or update an environment
**Status:** planned

**Operations:**
- **update**
  - Component: `environment`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `environment_name` eq `path.environment_name`
  - Notes:
    - Response body references #/components/schemas/environment
