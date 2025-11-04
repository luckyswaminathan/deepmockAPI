# Component Plan: `codespaces-public-key`

**API Slug:** `github`
**Total Routes:** 2

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (2)

#### `GET /orgs/{org}/codespaces/secrets/public-key`
**Summary:** Get an organization public key
**Status:** planned

**Operations:**
- **read_one**
  - Component: `codespaces-public-key`
  - Filters:
    - `org` eq `path.org`
  - Notes:
    - Response body references #/components/schemas/codespaces-public-key

#### `GET /repos/{owner}/{repo}/codespaces/secrets/public-key`
**Summary:** Get a repository public key
**Status:** planned

**Operations:**
- **read_one**
  - Component: `codespaces-public-key`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/codespaces-public-key
