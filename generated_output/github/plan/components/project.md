# Component Plan: `project`

**API Slug:** `github`
**Total Routes:** 15

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`update`**: Replace a full record.
- **`update_partial`**: Apply a partial update to a record.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (3)

#### `DELETE /orgs/{org}/teams/{team_slug}/projects/{project_id}`
**Summary:** Remove a project from a team
**Status:** planned

**Operations:**
- **delete**
  - Component: `project`
  - Filters:
    - `org` eq `path.org`
    - `team_slug` eq `path.team_slug`
    - `project_id` eq `path.project_id`

#### `DELETE /projects/{project_id}`
**Summary:** Delete a project
**Status:** planned

**Operations:**
- **delete**
  - Component: `project`
  - Filters:
    - `project_id` eq `path.project_id`

#### `DELETE /teams/{team_id}/projects/{project_id}`
**Summary:** Remove a project from a team (Legacy)
**Status:** planned

**Operations:**
- **delete**
  - Component: `project`
  - Filters:
    - `team_id` eq `path.team_id`
    - `project_id` eq `path.project_id`

### GET Routes (6)

#### `GET /orgs/{org}/projects`
**Summary:** List organization projects
**Status:** planned

**Operations:**
- **read_one**
  - Component: `project`
  - Filters:
    - `org` eq `path.org`
  - Notes:
    - Query parameters: state

#### `GET /orgs/{org}/teams/{team_slug}/projects`
**Summary:** List team projects
**Status:** planned

**Operations:**
- **read_one**
  - Component: `project`
  - Filters:
    - `org` eq `path.org`
    - `team_slug` eq `path.team_slug`

#### `GET /projects/{project_id}`
**Summary:** Get a project
**Status:** planned

**Operations:**
- **read_one**
  - Component: `project`
  - Filters:
    - `project_id` eq `path.project_id`
  - Notes:
    - Response body references #/components/schemas/project

#### `GET /repos/{owner}/{repo}/projects`
**Summary:** List repository projects
**Status:** planned

**Operations:**
- **read_one**
  - Component: `project`
  - Filters:
    - `owner_url` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Query parameters: state

#### `GET /teams/{team_id}/projects`
**Summary:** List team projects (Legacy)
**Status:** planned

**Operations:**
- **read_one**
  - Component: `project`
  - Filters:
    - `team_id` eq `path.team_id`

#### `GET /users/{username}/projects`
**Summary:** List user projects
**Status:** planned

**Operations:**
- **read_one**
  - Component: `project`
  - Filters:
    - `username` eq `path.username`
  - Notes:
    - Query parameters: state

### PATCH Routes (1)

#### `PATCH /projects/{project_id}`
**Summary:** Update a project
**Status:** planned

**Operations:**
- **update_partial**
  - Component: `project`
  - Filters:
    - `project_id` eq `path.project_id`
  - Notes:
    - Response body references #/components/schemas/project

### POST Routes (3)

#### `POST /orgs/{org}/projects`
**Summary:** Create an organization project
**Status:** planned

**Operations:**
- **create**
  - Component: `project`
  - Filters:
    - `org` eq `path.org`
  - Notes:
    - Response body references #/components/schemas/project

#### `POST /repos/{owner}/{repo}/projects`
**Summary:** Create a repository project
**Status:** planned

**Operations:**
- **create**
  - Component: `project`
  - Filters:
    - `owner_url` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/project

#### `POST /user/projects`
**Summary:** Create a user project
**Status:** planned

**Operations:**
- **create**
  - Component: `project`
  - Notes:
    - Response body references #/components/schemas/project

### PUT Routes (2)

#### `PUT /orgs/{org}/teams/{team_slug}/projects/{project_id}`
**Summary:** Add or update team project permissions
**Status:** planned

**Operations:**
- **update**
  - Component: `project`
  - Filters:
    - `org` eq `path.org`
    - `team_slug` eq `path.team_slug`
    - `project_id` eq `path.project_id`

#### `PUT /teams/{team_id}/projects/{project_id}`
**Summary:** Add or update team project permissions (Legacy)
**Status:** planned

**Operations:**
- **update**
  - Component: `project`
  - Filters:
    - `team_id` eq `path.team_id`
    - `project_id` eq `path.project_id`
