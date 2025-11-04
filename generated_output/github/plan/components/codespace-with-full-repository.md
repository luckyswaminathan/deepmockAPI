# Component Plan: `codespace-with-full-repository`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`create`**: Create a new record for the component.

## Routes

### POST Routes (1)

#### `POST /user/codespaces/{codespace_name}/publish`
**Summary:** Create a repository from an unpublished codespace
**Status:** planned

**Operations:**
- **create**
  - Component: `codespace-with-full-repository`
  - Filters:
    - `codespace_name` eq `path.codespace_name`
  - Notes:
    - Response body references #/components/schemas/codespace-with-full-repository
