# Component Plan: `repository-collaborator-permission`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/collaborators/{username}/permission`
**Summary:** Get repository permissions for a user
**Status:** planned

**Operations:**
- **read_one**
  - Component: `repository-collaborator-permission`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `username` eq `path.username`
  - Notes:
    - Response body references #/components/schemas/repository-collaborator-permission
