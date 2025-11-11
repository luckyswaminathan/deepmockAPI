# Component Plan: `starred-repository`

**API Slug:** `github`
**Total Routes:** 6

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.
- **`update`**: Replace a full record.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (1)

#### `DELETE /user/starred/{owner}/{repo}`
**Summary:** Unstar a repository for the authenticated user
**Status:** planned

**Operations:**
- **delete**
  - Component: `starred-repository`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`

### GET Routes (4)

#### `GET /gists/starred`
**Summary:** List starred gists
**Status:** planned

**Operations:**
- **read_many**
  - Component: `starred-repository`

#### `GET /user/starred`
**Summary:** List repositories starred by the authenticated user
**Status:** planned

**Operations:**
- **read_many**
  - Component: `starred-repository`

#### `GET /user/starred/{owner}/{repo}`
**Summary:** Check if a repository is starred by the authenticated user
**Status:** planned

**Operations:**
- **read_one**
  - Component: `starred-repository`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`

#### `GET /users/{username}/starred`
**Summary:** List repositories starred by a user
**Status:** planned

**Operations:**
- **read_one**
  - Component: `starred-repository`
  - Filters:
    - `username` eq `path.username`

### PUT Routes (1)

#### `PUT /user/starred/{owner}/{repo}`
**Summary:** Star a repository for the authenticated user
**Status:** planned

**Operations:**
- **update**
  - Component: `starred-repository`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
