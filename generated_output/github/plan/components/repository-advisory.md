# Component Plan: `repository-advisory`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/security-advisories/{ghsa_id}`
**Summary:** Get a repository security advisory
**Status:** planned

**Operations:**
- **read_one**
  - Component: `repository-advisory`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `ghsa_id` eq `path.ghsa_id`
  - Notes:
    - Response body references #/components/schemas/repository-advisory
