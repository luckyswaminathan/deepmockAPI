# Component Plan: `key`

**API Slug:** `github`
**Total Routes:** 7

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (2)

#### `DELETE /repos/{owner}/{repo}/keys/{key_id}`
**Summary:** Delete a deploy key
**Status:** planned

**Operations:**
- **delete**
  - Component: `key`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `key_id` eq `path.key_id`

#### `DELETE /user/keys/{key_id}`
**Summary:** Delete a public SSH key for the authenticated user
**Status:** planned

**Operations:**
- **delete**
  - Component: `key`
  - Filters:
    - `key_id` eq `path.key_id`

### GET Routes (4)

#### `GET /repos/{owner}/{repo}/keys`
**Summary:** List deploy keys
**Status:** planned

**Operations:**
- **read_one**
  - Component: `key`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`

#### `GET /user/keys`
**Summary:** List public SSH keys for the authenticated user
**Status:** planned

**Operations:**
- **read_many**
  - Component: `key`

#### `GET /user/keys/{key_id}`
**Summary:** Get a public SSH key for the authenticated user
**Status:** planned

**Operations:**
- **read_one**
  - Component: `key`
  - Filters:
    - `key_id` eq `path.key_id`
  - Notes:
    - Response body references #/components/schemas/key

#### `GET /users/{username}/keys`
**Summary:** List public keys for a user
**Status:** planned

**Operations:**
- **read_one**
  - Component: `key`
  - Filters:
    - `username` eq `path.username`

### POST Routes (1)

#### `POST /user/keys`
**Summary:** Create a public SSH key for the authenticated user
**Status:** planned

**Operations:**
- **create**
  - Component: `key`
  - Notes:
    - Response body references #/components/schemas/key
