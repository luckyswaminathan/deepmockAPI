# Component Plan: `community-profile`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/community/profile`
**Summary:** Get community profile metrics
**Status:** planned

**Operations:**
- **read_one**
  - Component: `community-profile`
  - Filters:
    - `owner` eq `path.owner`
    - `content_reports_enabled` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/community-profile
