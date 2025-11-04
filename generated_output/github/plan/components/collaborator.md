# Component Plan: `collaborator`

**API Slug:** `github`
**Total Routes:** 6

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.
- **`update`**: Replace a full record.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (2)

#### `DELETE /projects/{project_id}/collaborators/{username}`
**Summary:** Remove user as a collaborator
**Status:** planned

**Operations:**
- **delete**
  - Component: `collaborator`
  - Filters:
    - `project_id` eq `path.project_id`
    - `username` eq `path.username`

#### `DELETE /repos/{owner}/{repo}/collaborators/{username}`
**Summary:** Remove a repository collaborator
**Status:** planned

**Operations:**
- **delete**
  - Component: `collaborator`
  - Filters:
    - `owner` eq `path.owner`
    - `repos_url` eq `path.repo`
    - `username` eq `path.username`

### GET Routes (3)

#### `GET /projects/{project_id}/collaborators`
**Summary:** List project collaborators
**Status:** planned

**Operations:**
- **read_one**
  - Component: `collaborator`
  - Filters:
    - `project_id` eq `path.project_id`
  - Notes:
    - Query parameters: affiliation

#### `GET /repos/{owner}/{repo}/collaborators`
**Summary:** List repository collaborators
**Status:** planned

**Operations:**
- **read_one**
  - Component: `collaborator`
  - Filters:
    - `owner` eq `path.owner`
    - `repos_url` eq `path.repo`
  - Notes:
    - Query parameters: affiliation, permission

#### `GET /repos/{owner}/{repo}/collaborators/{username}`
**Summary:** Check if a user is a repository collaborator
**Status:** planned

**Operations:**
- **read_one**
  - Component: `collaborator`
  - Filters:
    - `owner` eq `path.owner`
    - `repos_url` eq `path.repo`
    - `username` eq `path.username`

### PUT Routes (1)

#### `PUT /projects/{project_id}/collaborators/{username}`
**Summary:** Add project collaborator
**Status:** planned

**Operations:**
- **update**
  - Component: `collaborator`
  - Filters:
    - `project_id` eq `path.project_id`
    - `username` eq `path.username`
