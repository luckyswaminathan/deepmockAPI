# Component Plan: `actions-secret`

**API Slug:** `github`
**Total Routes:** 2

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (2)

#### `GET /repos/{owner}/{repo}/actions/secrets/{secret_name}`
**Summary:** Get a repository secret
**Status:** planned

**Operations:**
- **read_one**
  - Component: `actions-secret`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `secret_name` eq `path.secret_name`
  - Notes:
    - Response body references #/components/schemas/actions-secret

#### `GET /repos/{owner}/{repo}/environments/{environment_name}/secrets/{secret_name}`
**Summary:** Get an environment secret
**Status:** planned

**Operations:**
- **read_one**
  - Component: `actions-secret`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `environment_name` eq `path.environment_name`
    - `secret_name` eq `path.secret_name`
  - Notes:
    - Response body references #/components/schemas/actions-secret
