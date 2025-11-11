# Component Plan: `code-scanning-default-setup`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/code-scanning/default-setup`
**Summary:** Get a code scanning default setup configuration
**Status:** planned

**Operations:**
- **read_one**
  - Component: `code-scanning-default-setup`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/code-scanning-default-setup
