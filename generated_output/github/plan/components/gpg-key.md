# Component Plan: `gpg-key`

**API Slug:** `github`
**Total Routes:** 2

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /user/gpg_keys/{gpg_key_id}`
**Summary:** Get a GPG key for the authenticated user
**Status:** planned

**Operations:**
- **read_one**
  - Component: `gpg-key`
  - Filters:
    - `gpg_key_id` eq `path.gpg_key_id`
  - Notes:
    - Response body references #/components/schemas/gpg-key

### POST Routes (1)

#### `POST /user/gpg_keys`
**Summary:** Create a GPG key for the authenticated user
**Status:** planned

**Operations:**
- **create**
  - Component: `gpg-key`
  - Notes:
    - Response body references #/components/schemas/gpg-key
