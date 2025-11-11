# Component Plan: `check-suite-preference`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`update_partial`**: Apply a partial update to a record.

## Routes

### PATCH Routes (1)

#### `PATCH /repos/{owner}/{repo}/check-suites/preferences`
**Summary:** Update repository preferences for check suites
**Status:** planned

**Operations:**
- **update_partial**
  - Component: `check-suite-preference`
  - Filters:
    - `owner` eq `path.owner`
    - `repository` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/check-suite-preference
