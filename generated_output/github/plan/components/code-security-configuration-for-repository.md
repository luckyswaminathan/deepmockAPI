# Component Plan: `code-security-configuration-for-repository`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/code-security-configuration`
**Summary:** Get the code security configuration associated with a repository
**Status:** planned

**Operations:**
- **read_one**
  - Component: `code-security-configuration-for-repository`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/code-security-configuration-for-repository
