# Component Plan: `discussion`

**API Slug:** `github`
**Total Routes:** 4

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (2)

#### `DELETE /orgs/{org}/teams/{team_slug}/discussions/{discussion_number}`
**Summary:** Delete a discussion
**Status:** planned

**Operations:**
- **delete**
  - Component: `discussion`
  - Filters:
    - `org` eq `path.org`
    - `team_slug` eq `path.team_slug`
    - `discussion_number` eq `path.discussion_number`

#### `DELETE /teams/{team_id}/discussions/{discussion_number}`
**Summary:** Delete a discussion (Legacy)
**Status:** planned

**Operations:**
- **delete**
  - Component: `discussion`
  - Filters:
    - `team_id` eq `path.team_id`
    - `discussion_number` eq `path.discussion_number`

### GET Routes (2)

#### `GET /orgs/{org}/teams/{team_slug}/discussions`
**Summary:** List discussions
**Status:** planned

**Operations:**
- **read_one**
  - Component: `discussion`
  - Filters:
    - `org` eq `path.org`
    - `team_slug` eq `path.team_slug`
  - Notes:
    - Query parameters: pinned

#### `GET /teams/{team_id}/discussions`
**Summary:** List discussions (Legacy)
**Status:** planned

**Operations:**
- **read_one**
  - Component: `discussion`
  - Filters:
    - `team_id` eq `path.team_id`
