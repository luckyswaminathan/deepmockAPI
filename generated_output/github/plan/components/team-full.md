# Component Plan: `team-full`

**API Slug:** `github`
**Total Routes:** 5

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`update_partial`**: Apply a partial update to a record.

## Routes

### GET Routes (2)

#### `GET /orgs/{org}/teams/{team_slug}`
**Summary:** Get a team by name
**Status:** planned

**Operations:**
- **read_one**
  - Component: `team-full`
  - Filters:
    - `org` eq `path.org`
    - `team_slug` eq `path.team_slug`
  - Notes:
    - Response body references #/components/schemas/team-full

#### `GET /teams/{team_id}`
**Summary:** Get a team (Legacy)
**Status:** planned

**Operations:**
- **read_one**
  - Component: `team-full`
  - Filters:
    - `team_id` eq `path.team_id`
  - Notes:
    - Response body references #/components/schemas/team-full

### PATCH Routes (2)

#### `PATCH /orgs/{org}/teams/{team_slug}`
**Summary:** Update a team
**Status:** planned

**Operations:**
- **update_partial**
  - Component: `team-full`
  - Filters:
    - `org` eq `path.org`
    - `team_slug` eq `path.team_slug`
  - Notes:
    - Response body references #/components/schemas/team-full

#### `PATCH /teams/{team_id}`
**Summary:** Update a team (Legacy)
**Status:** planned

**Operations:**
- **update_partial**
  - Component: `team-full`
  - Filters:
    - `team_id` eq `path.team_id`
  - Notes:
    - Response body references #/components/schemas/team-full

### POST Routes (1)

#### `POST /orgs/{org}/teams`
**Summary:** Create a team
**Status:** planned

**Operations:**
- **create**
  - Component: `team-full`
  - Filters:
    - `org` eq `path.org`
  - Notes:
    - Response body references #/components/schemas/team-full
