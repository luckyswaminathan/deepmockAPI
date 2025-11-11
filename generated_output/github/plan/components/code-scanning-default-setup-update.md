# Component Plan: `code-scanning-default-setup-update`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`update_partial`**: Apply a partial update to a record.

## Routes

### PATCH Routes (1)

#### `PATCH /repos/{owner}/{repo}/code-scanning/default-setup`
**Summary:** Update a code scanning default setup configuration
**Status:** planned

**Operations:**
- **update_partial**
  - Component: `code-scanning-default-setup-update`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Request body references #/components/schemas/code-scanning-default-setup-update
    - Response body references #/components/schemas/empty-object
