# Component Plan: `hook`

**API Slug:** `github`
**Total Routes:** 7

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`update_partial`**: Apply a partial update to a record.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (2)

#### `DELETE /orgs/{org}/hooks/{hook_id}`
**Summary:** Delete an organization webhook
**Status:** planned

**Operations:**
- **delete**
  - Component: `hook`
  - Filters:
    - `org` eq `path.org`
    - `hook_id` eq `path.hook_id`

#### `DELETE /repos/{owner}/{repo}/hooks/{hook_id}`
**Summary:** Delete a repository webhook
**Status:** planned

**Operations:**
- **delete**
  - Component: `hook`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `hook_id` eq `path.hook_id`

### GET Routes (3)

#### `GET /orgs/{org}/hooks`
**Summary:** List organization webhooks
**Status:** planned

**Operations:**
- **read_one**
  - Component: `hook`
  - Filters:
    - `org` eq `path.org`

#### `GET /repos/{owner}/{repo}/hooks`
**Summary:** List repository webhooks
**Status:** planned

**Operations:**
- **read_one**
  - Component: `hook`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`

#### `GET /repos/{owner}/{repo}/hooks/{hook_id}`
**Summary:** Get a repository webhook
**Status:** planned

**Operations:**
- **read_one**
  - Component: `hook`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `hook_id` eq `path.hook_id`
  - Notes:
    - Response body references #/components/schemas/hook

### PATCH Routes (1)

#### `PATCH /repos/{owner}/{repo}/hooks/{hook_id}`
**Summary:** Update a repository webhook
**Status:** planned

**Operations:**
- **update_partial**
  - Component: `hook`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `hook_id` eq `path.hook_id`
  - Notes:
    - Response body references #/components/schemas/hook

### POST Routes (1)

#### `POST /repos/{owner}/{repo}/hooks`
**Summary:** Create a repository webhook
**Status:** planned

**Operations:**
- **create**
  - Component: `hook`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/hook
