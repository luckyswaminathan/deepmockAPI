# Component Plan: `team-membership`

**API Slug:** `github`
**Total Routes:** 4

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.
- **`update`**: Replace a full record.

## Routes

### GET Routes (2)

#### `GET /orgs/{org}/teams/{team_slug}/memberships/{username}`
**Summary:** Get team membership for a user
**Status:** planned

**Operations:**
- **read_one**
  - Component: `team-membership`
  - Filters:
    - `org` eq `path.org`
    - `team_slug` eq `path.team_slug`
    - `username` eq `path.username`
  - Notes:
    - Response body references #/components/schemas/team-membership

#### `GET /teams/{team_id}/memberships/{username}`
**Summary:** Get team membership for a user (Legacy)
**Status:** planned

**Operations:**
- **read_one**
  - Component: `team-membership`
  - Filters:
    - `team_id` eq `path.team_id`
    - `username` eq `path.username`
  - Notes:
    - Response body references #/components/schemas/team-membership

### PUT Routes (2)

#### `PUT /orgs/{org}/teams/{team_slug}/memberships/{username}`
**Summary:** Add or update team membership for a user
**Status:** planned

**Operations:**
- **update**
  - Component: `team-membership`
  - Filters:
    - `org` eq `path.org`
    - `team_slug` eq `path.team_slug`
    - `username` eq `path.username`
  - Notes:
    - Response body references #/components/schemas/team-membership

#### `PUT /teams/{team_id}/memberships/{username}`
**Summary:** Add or update team membership for a user (Legacy)
**Status:** planned

**Operations:**
- **update**
  - Component: `team-membership`
  - Filters:
    - `team_id` eq `path.team_id`
    - `username` eq `path.username`
  - Notes:
    - Response body references #/components/schemas/team-membership
