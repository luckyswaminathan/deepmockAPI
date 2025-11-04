# Component Plan: `ssh-signing-key`

**API Slug:** `github`
**Total Routes:** 2

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /user/ssh_signing_keys/{ssh_signing_key_id}`
**Summary:** Get an SSH signing key for the authenticated user
**Status:** planned

**Operations:**
- **read_one**
  - Component: `ssh-signing-key`
  - Filters:
    - `ssh_signing_key_id` eq `path.ssh_signing_key_id`
  - Notes:
    - Response body references #/components/schemas/ssh-signing-key

### POST Routes (1)

#### `POST /user/ssh_signing_keys`
**Summary:** Create a SSH signing key for the authenticated user
**Status:** planned

**Operations:**
- **create**
  - Component: `ssh-signing-key`
  - Notes:
    - Response body references #/components/schemas/ssh-signing-key
