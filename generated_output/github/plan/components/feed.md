# Component Plan: `feed`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_many`**: List or search records.

## Routes

### GET Routes (1)

#### `GET /feeds`
**Summary:** Get feeds
**Status:** planned

**Operations:**
- **read_many**
  - Component: `feed`
  - Notes:
    - Response body references #/components/schemas/feed
