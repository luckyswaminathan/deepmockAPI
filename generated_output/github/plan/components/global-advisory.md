# Component Plan: `global-advisory`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /advisories/{ghsa_id}`
**Summary:** Get a global security advisory
**Status:** planned

**Operations:**
- **read_one**
  - Component: `global-advisory`
  - Filters:
    - `ghsa_id` eq `path.ghsa_id`
  - Notes:
    - Response body references #/components/schemas/global-advisory
