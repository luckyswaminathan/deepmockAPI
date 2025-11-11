# Component Plan: `secret-scanning-push-protection-bypass`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`create`**: Create a new record for the component.

## Routes

### POST Routes (1)

#### `POST /repos/{owner}/{repo}/secret-scanning/push-protection-bypasses`
**Summary:** Create a push protection bypass
**Status:** planned

**Operations:**
- **create**
  - Component: `secret-scanning-push-protection-bypass`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/secret-scanning-push-protection-bypass
