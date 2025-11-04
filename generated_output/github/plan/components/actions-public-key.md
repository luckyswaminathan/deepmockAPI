# Component Plan: `actions-public-key`

**API Slug:** `github`
**Total Routes:** 3

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (3)

#### `GET /orgs/{org}/actions/secrets/public-key`
**Summary:** Get an organization public key
**Status:** planned

**Operations:**
- **read_one**
  - Component: `actions-public-key`
  - Filters:
    - `org` eq `path.org`
  - Notes:
    - Response body references #/components/schemas/actions-public-key

#### `GET /repos/{owner}/{repo}/actions/secrets/public-key`
**Summary:** Get a repository public key
**Status:** planned

**Operations:**
- **read_one**
  - Component: `actions-public-key`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/actions-public-key

#### `GET /repos/{owner}/{repo}/environments/{environment_name}/secrets/public-key`
**Summary:** Get an environment public key
**Status:** planned

**Operations:**
- **read_one**
  - Component: `actions-public-key`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `environment_name` eq `path.environment_name`
  - Notes:
    - Response body references #/components/schemas/actions-public-key
