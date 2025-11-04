# Component Plan: `api-overview`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_many`**: List or search records.

## Routes

### GET Routes (1)

#### `GET /meta`
**Summary:** Get GitHub meta information
**Status:** planned

**Operations:**
- **read_many**
  - Component: `api-overview`
  - Notes:
    - Response body references #/components/schemas/api-overview
