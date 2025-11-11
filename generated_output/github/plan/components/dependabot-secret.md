# Component Plan: `dependabot-secret`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/dependabot/secrets/{secret_name}`
**Summary:** Get a repository secret
**Status:** planned

**Operations:**
- **read_one**
  - Component: `dependabot-secret`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `secret_name` eq `path.secret_name`
  - Notes:
    - Response body references #/components/schemas/dependabot-secret
