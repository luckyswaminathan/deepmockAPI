# Component Plan: `stargazer`

**API Slug:** `github`
**Total Routes:** 4

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.
- **`update`**: Replace a full record.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (1)

#### `DELETE /gists/{gist_id}/star`
**Summary:** Unstar a gist
**Status:** planned

**Operations:**
- **delete**
  - Component: `stargazer`
  - Filters:
    - `gist_id` eq `path.gist_id`

### GET Routes (2)

#### `GET /gists/{gist_id}/star`
**Summary:** Check if a gist is starred
**Status:** planned

**Operations:**
- **read_one**
  - Component: `stargazer`
  - Filters:
    - `gist_id` eq `path.gist_id`

#### `GET /repos/{owner}/{repo}/stargazers`
**Summary:** List stargazers
**Status:** planned

**Operations:**
- **read_one**
  - Component: `stargazer`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`

### PUT Routes (1)

#### `PUT /gists/{gist_id}/star`
**Summary:** Star a gist
**Status:** planned

**Operations:**
- **update**
  - Component: `stargazer`
  - Filters:
    - `gist_id` eq `path.gist_id`
