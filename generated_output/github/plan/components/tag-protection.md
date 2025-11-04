# Component Plan: `tag-protection`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`create`**: Create a new record for the component.

## Routes

### POST Routes (1)

#### `POST /repos/{owner}/{repo}/tags/protection`
**Summary:** Deprecated - Create a tag protection state for a repository
**Status:** planned

**Operations:**
- **create**
  - Component: `tag-protection`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/tag-protection
