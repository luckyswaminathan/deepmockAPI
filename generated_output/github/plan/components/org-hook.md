# Component Plan: `org-hook`

**API Slug:** `github`
**Total Routes:** 3

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`update_partial`**: Apply a partial update to a record.

## Routes

### GET Routes (1)

#### `GET /orgs/{org}/hooks/{hook_id}`
**Summary:** Get an organization webhook
**Status:** planned

**Operations:**
- **read_one**
  - Component: `org-hook`
  - Filters:
    - `org` eq `path.org`
    - `hook_id` eq `path.hook_id`
  - Notes:
    - Response body references #/components/schemas/org-hook

### PATCH Routes (1)

#### `PATCH /orgs/{org}/hooks/{hook_id}`
**Summary:** Update an organization webhook
**Status:** planned

**Operations:**
- **update_partial**
  - Component: `org-hook`
  - Filters:
    - `org` eq `path.org`
    - `hook_id` eq `path.hook_id`
  - Notes:
    - Response body references #/components/schemas/org-hook

### POST Routes (1)

#### `POST /orgs/{org}/hooks`
**Summary:** Create an organization webhook
**Status:** planned

**Operations:**
- **create**
  - Component: `org-hook`
  - Filters:
    - `org` eq `path.org`
  - Notes:
    - Response body references #/components/schemas/org-hook
