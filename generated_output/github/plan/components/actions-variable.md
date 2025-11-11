# Component Plan: `actions-variable`

**API Slug:** `github`
**Total Routes:** 2

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (2)

#### `GET /repos/{owner}/{repo}/actions/variables/{name}`
**Summary:** Get a repository variable
**Status:** planned

**Operations:**
- **read_one**
  - Component: `actions-variable`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `name` eq `path.name`
  - Notes:
    - Response body references #/components/schemas/actions-variable

#### `GET /repos/{owner}/{repo}/environments/{environment_name}/variables/{name}`
**Summary:** Get an environment variable
**Status:** planned

**Operations:**
- **read_one**
  - Component: `actions-variable`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `environment_name` eq `path.environment_name`
    - `name` eq `path.name`
  - Notes:
    - Response body references #/components/schemas/actions-variable
