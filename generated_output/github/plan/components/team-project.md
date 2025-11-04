# Component Plan: `team-project`

**API Slug:** `github`
**Total Routes:** 2

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (2)

#### `GET /orgs/{org}/teams/{team_slug}/projects/{project_id}`
**Summary:** Check team permissions for a project
**Status:** planned

**Operations:**
- **read_one**
  - Component: `team-project`
  - Filters:
    - `org` eq `path.org`
    - `team_slug` eq `path.team_slug`
    - `project_id` eq `path.project_id`
  - Notes:
    - Response body references #/components/schemas/team-project

#### `GET /teams/{team_id}/projects/{project_id}`
**Summary:** Check team permissions for a project (Legacy)
**Status:** planned

**Operations:**
- **read_one**
  - Component: `team-project`
  - Filters:
    - `team_id` eq `path.team_id`
    - `project_id` eq `path.project_id`
  - Notes:
    - Response body references #/components/schemas/team-project
