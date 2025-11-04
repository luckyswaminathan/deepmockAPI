# Component Plan: `team`

**API Slug:** `github`
**Total Routes:** 18

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.
- **`update`**: Replace a full record.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (6)

#### `DELETE /orgs/{org}/organization-roles/teams/{team_slug}`
**Summary:** Remove all organization roles for a team
**Status:** planned

**Operations:**
- **delete**
  - Component: `team`
  - Filters:
    - `org` eq `path.org`
    - `team_slug` eq `path.team_slug`

#### `DELETE /orgs/{org}/organization-roles/teams/{team_slug}/{role_id}`
**Summary:** Remove an organization role from a team
**Status:** planned

**Operations:**
- **delete**
  - Component: `team`
  - Filters:
    - `org` eq `path.org`
    - `team_slug` eq `path.team_slug`
    - `role_id` eq `path.role_id`

#### `DELETE /orgs/{org}/security-managers/teams/{team_slug}`
**Summary:** Remove a security manager team
**Status:** planned

**Operations:**
- **delete**
  - Component: `team`
  - Filters:
    - `org` eq `path.org`
    - `team_slug` eq `path.team_slug`

#### `DELETE /orgs/{org}/teams/{team_slug}`
**Summary:** Delete a team
**Status:** planned

**Operations:**
- **delete**
  - Component: `team`
  - Filters:
    - `org` eq `path.org`
    - `team_slug` eq `path.team_slug`

#### `DELETE /repos/{owner}/{repo}/branches/{branch}/protection/restrictions/teams`
**Summary:** Remove team access restrictions
**Status:** planned

**Operations:**
- **delete**
  - Component: `team`
  - Filters:
    - `owner` eq `path.owner`
    - `repositories_url` eq `path.repo`
    - `branch` eq `path.branch`

#### `DELETE /teams/{team_id}`
**Summary:** Delete a team (Legacy)
**Status:** planned

**Operations:**
- **delete**
  - Component: `team`
  - Filters:
    - `team_id` eq `path.team_id`

### GET Routes (8)

#### `GET /orgs/{org}/invitations/{invitation_id}/teams`
**Summary:** List organization invitation teams
**Status:** planned

**Operations:**
- **read_one**
  - Component: `team`
  - Filters:
    - `org` eq `path.org`
    - `invitation_id` eq `path.invitation_id`

#### `GET /orgs/{org}/organization-roles/{role_id}/teams`
**Summary:** List teams that are assigned to an organization role
**Status:** planned

**Operations:**
- **read_one**
  - Component: `team`
  - Filters:
    - `org` eq `path.org`
    - `role_id` eq `path.role_id`

#### `GET /orgs/{org}/teams`
**Summary:** List teams
**Status:** planned

**Operations:**
- **read_one**
  - Component: `team`
  - Filters:
    - `org` eq `path.org`

#### `GET /orgs/{org}/teams/{team_slug}/teams`
**Summary:** List child teams
**Status:** planned

**Operations:**
- **read_one**
  - Component: `team`
  - Filters:
    - `org` eq `path.org`
    - `team_slug` eq `path.team_slug`

#### `GET /repos/{owner}/{repo}/branches/{branch}/protection/restrictions/teams`
**Summary:** Get teams with access to the protected branch
**Status:** planned

**Operations:**
- **read_one**
  - Component: `team`
  - Filters:
    - `owner` eq `path.owner`
    - `repositories_url` eq `path.repo`
    - `branch` eq `path.branch`

#### `GET /repos/{owner}/{repo}/teams`
**Summary:** List repository teams
**Status:** planned

**Operations:**
- **read_one**
  - Component: `team`
  - Filters:
    - `owner` eq `path.owner`
    - `repositories_url` eq `path.repo`

#### `GET /teams/{team_id}/teams`
**Summary:** List child teams (Legacy)
**Status:** planned

**Operations:**
- **read_one**
  - Component: `team`
  - Filters:
    - `team_id` eq `path.team_id`

#### `GET /user/teams`
**Summary:** List teams for the authenticated user
**Status:** planned

**Operations:**
- **read_many**
  - Component: `team`

### POST Routes (1)

#### `POST /repos/{owner}/{repo}/branches/{branch}/protection/restrictions/teams`
**Summary:** Add team access restrictions
**Status:** planned

**Operations:**
- **create**
  - Component: `team`
  - Filters:
    - `owner` eq `path.owner`
    - `repositories_url` eq `path.repo`
    - `branch` eq `path.branch`

### PUT Routes (3)

#### `PUT /orgs/{org}/organization-roles/teams/{team_slug}/{role_id}`
**Summary:** Assign an organization role to a team
**Status:** planned

**Operations:**
- **update**
  - Component: `team`
  - Filters:
    - `org` eq `path.org`
    - `team_slug` eq `path.team_slug`
    - `role_id` eq `path.role_id`

#### `PUT /orgs/{org}/security-managers/teams/{team_slug}`
**Summary:** Add a security manager team
**Status:** planned

**Operations:**
- **update**
  - Component: `team`
  - Filters:
    - `org` eq `path.org`
    - `team_slug` eq `path.team_slug`

#### `PUT /repos/{owner}/{repo}/branches/{branch}/protection/restrictions/teams`
**Summary:** Set team access restrictions
**Status:** planned

**Operations:**
- **update**
  - Component: `team`
  - Filters:
    - `owner` eq `path.owner`
    - `repositories_url` eq `path.repo`
    - `branch` eq `path.branch`
