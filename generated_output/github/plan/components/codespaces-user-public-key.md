# Component Plan: `codespaces-user-public-key`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_many`**: List or search records.

## Routes

### GET Routes (1)

#### `GET /user/codespaces/secrets/public-key`
**Summary:** Get public key for the authenticated user
**Status:** planned

**Operations:**
- **read_many**
  - Component: `codespaces-user-public-key`
  - Notes:
    - Response body references #/components/schemas/codespaces-user-public-key
