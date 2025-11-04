# Component Plan: `user-marketplace-purchase`

**API Slug:** `github`
**Total Routes:** 2

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.

## Routes

### GET Routes (2)

#### `GET /user`
**Summary:** Get the authenticated user
**Status:** planned

**Operations:**
- **read_many**
  - Component: `user-marketplace-purchase`

#### `GET /user/{account_id}`
**Summary:** Get a user using their ID
**Status:** planned

**Operations:**
- **read_one**
  - Component: `user-marketplace-purchase`
  - Filters:
    - `account_id` eq `path.account_id`
