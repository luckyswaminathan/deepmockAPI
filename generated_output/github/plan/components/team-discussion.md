# Component Plan: `team-discussion`

**API Slug:** `github`
**Total Routes:** 6

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`update_partial`**: Apply a partial update to a record.

## Routes

### GET Routes (2)

#### `GET /orgs/{org}/teams/{team_slug}/discussions/{discussion_number}`
**Summary:** Get a discussion
**Status:** planned

**Operations:**
- **read_one**
  - Component: `team-discussion`
  - Filters:
    - `org` eq `path.org`
    - `team_slug` eq `path.team_slug`
    - `discussion_number` eq `path.discussion_number`
  - Notes:
    - Response body references #/components/schemas/team-discussion

#### `GET /teams/{team_id}/discussions/{discussion_number}`
**Summary:** Get a discussion (Legacy)
**Status:** planned

**Operations:**
- **read_one**
  - Component: `team-discussion`
  - Filters:
    - `team_id` eq `path.team_id`
    - `discussion_number` eq `path.discussion_number`
  - Notes:
    - Response body references #/components/schemas/team-discussion

### PATCH Routes (2)

#### `PATCH /orgs/{org}/teams/{team_slug}/discussions/{discussion_number}`
**Summary:** Update a discussion
**Status:** planned

**Operations:**
- **update_partial**
  - Component: `team-discussion`
  - Filters:
    - `org` eq `path.org`
    - `team_slug` eq `path.team_slug`
    - `discussion_number` eq `path.discussion_number`
  - Notes:
    - Response body references #/components/schemas/team-discussion

#### `PATCH /teams/{team_id}/discussions/{discussion_number}`
**Summary:** Update a discussion (Legacy)
**Status:** planned

**Operations:**
- **update_partial**
  - Component: `team-discussion`
  - Filters:
    - `team_id` eq `path.team_id`
    - `discussion_number` eq `path.discussion_number`
  - Notes:
    - Response body references #/components/schemas/team-discussion

### POST Routes (2)

#### `POST /orgs/{org}/teams/{team_slug}/discussions`
**Summary:** Create a discussion
**Status:** planned

**Operations:**
- **create**
  - Component: `team-discussion`
  - Filters:
    - `org` eq `path.org`
    - `team_slug` eq `path.team_slug`
  - Notes:
    - Response body references #/components/schemas/team-discussion

#### `POST /teams/{team_id}/discussions`
**Summary:** Create a discussion (Legacy)
**Status:** planned

**Operations:**
- **create**
  - Component: `team-discussion`
  - Filters:
    - `team_id` eq `path.team_id`
  - Notes:
    - Response body references #/components/schemas/team-discussion
