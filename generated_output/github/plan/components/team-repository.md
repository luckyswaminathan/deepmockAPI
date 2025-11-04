# Component Plan: `team-repository`

**API Slug:** `github`
**Total Routes:** 2

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (2)

#### `GET /orgs/{org}/teams/{team_slug}/repos/{owner}/{repo}`
**Summary:** Check team permissions for a repository
**Status:** planned

**Operations:**
- **read_one**
  - Component: `team-repository`
  - Filters:
    - `org` eq `path.org`
    - `team_slug` eq `path.team_slug`
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/team-repository

#### `GET /teams/{team_id}/repos/{owner}/{repo}`
**Summary:** Check team permissions for a repository (Legacy)
**Status:** planned

**Operations:**
- **read_one**
  - Component: `team-repository`
  - Filters:
    - `team_id` eq `path.team_id`
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/team-repository
