# Component Plan: `repository-advisory-update`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`update_partial`**: Apply a partial update to a record.

## Routes

### PATCH Routes (1)

#### `PATCH /repos/{owner}/{repo}/security-advisories/{ghsa_id}`
**Summary:** Update a repository security advisory
**Status:** planned

**Operations:**
- **update_partial**
  - Component: `repository-advisory-update`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `ghsa_id` eq `path.ghsa_id`
  - Notes:
    - Request body references #/components/schemas/repository-advisory-update
    - Response body references #/components/schemas/repository-advisory
