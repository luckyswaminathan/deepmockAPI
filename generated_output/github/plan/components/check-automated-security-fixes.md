# Component Plan: `check-automated-security-fixes`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/automated-security-fixes`
**Summary:** Check if automated security fixes are enabled for a repository
**Status:** planned

**Operations:**
- **read_one**
  - Component: `check-automated-security-fixes`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/check-automated-security-fixes
