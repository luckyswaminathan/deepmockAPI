# Component Plan: `protected-branch`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`update`**: Replace a full record.

## Routes

### PUT Routes (1)

#### `PUT /repos/{owner}/{repo}/branches/{branch}/protection`
**Summary:** Update branch protection
**Status:** planned

**Operations:**
- **update**
  - Component: `protected-branch`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `lock_branch` eq `path.branch`
  - Notes:
    - Response body references #/components/schemas/protected-branch
