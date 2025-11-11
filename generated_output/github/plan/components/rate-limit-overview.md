# Component Plan: `rate-limit-overview`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_many`**: List or search records.

## Routes

### GET Routes (1)

#### `GET /rate_limit`
**Summary:** Get rate limit status for the authenticated user
**Status:** planned

**Operations:**
- **read_many**
  - Component: `rate-limit-overview`
  - Notes:
    - Response body references #/components/schemas/rate-limit-overview
