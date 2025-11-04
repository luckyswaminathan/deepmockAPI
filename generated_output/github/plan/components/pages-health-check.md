# Component Plan: `pages-health-check`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/pages/health`
**Summary:** Get a DNS health check for GitHub Pages
**Status:** planned

**Operations:**
- **read_one**
  - Component: `pages-health-check`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/pages-health-check
