# Component Plan: `webhook-config`

**API Slug:** `github`
**Total Routes:** 6

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.
- **`update_partial`**: Apply a partial update to a record.

## Routes

### GET Routes (3)

#### `GET /app/hook/config`
**Summary:** Get a webhook configuration for an app
**Status:** planned

**Operations:**
- **read_many**
  - Component: `webhook-config`
  - Notes:
    - Response body references #/components/schemas/webhook-config

#### `GET /orgs/{org}/hooks/{hook_id}/config`
**Summary:** Get a webhook configuration for an organization
**Status:** planned

**Operations:**
- **read_one**
  - Component: `webhook-config`
  - Filters:
    - `org` eq `path.org`
    - `hook_id` eq `path.hook_id`
  - Notes:
    - Response body references #/components/schemas/webhook-config

#### `GET /repos/{owner}/{repo}/hooks/{hook_id}/config`
**Summary:** Get a webhook configuration for a repository
**Status:** planned

**Operations:**
- **read_one**
  - Component: `webhook-config`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `hook_id` eq `path.hook_id`
  - Notes:
    - Response body references #/components/schemas/webhook-config

### PATCH Routes (3)

#### `PATCH /app/hook/config`
**Summary:** Update a webhook configuration for an app
**Status:** planned

**Operations:**
- **update_partial**
  - Component: `webhook-config`
  - Notes:
    - Response body references #/components/schemas/webhook-config

#### `PATCH /orgs/{org}/hooks/{hook_id}/config`
**Summary:** Update a webhook configuration for an organization
**Status:** planned

**Operations:**
- **update_partial**
  - Component: `webhook-config`
  - Filters:
    - `org` eq `path.org`
    - `hook_id` eq `path.hook_id`
  - Notes:
    - Response body references #/components/schemas/webhook-config

#### `PATCH /repos/{owner}/{repo}/hooks/{hook_id}/config`
**Summary:** Update a webhook configuration for a repository
**Status:** planned

**Operations:**
- **update_partial**
  - Component: `webhook-config`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `hook_id` eq `path.hook_id`
  - Notes:
    - Response body references #/components/schemas/webhook-config
