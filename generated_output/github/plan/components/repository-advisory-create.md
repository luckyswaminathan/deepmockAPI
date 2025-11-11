# Component Plan: `repository-advisory-create`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`create`**: Create a new record for the component.

## Routes

### POST Routes (1)

#### `POST /repos/{owner}/{repo}/security-advisories`
**Summary:** Create a repository security advisory
**Status:** planned

**Operations:**
- **create**
  - Component: `repository-advisory-create`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Request body references #/components/schemas/repository-advisory-create
    - Response body references #/components/schemas/repository-advisory
