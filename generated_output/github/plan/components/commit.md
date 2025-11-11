# Component Plan: `commit`

**API Slug:** `github`
**Total Routes:** 6

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.

## Routes

### GET Routes (5)

#### `GET /gists/{gist_id}/commits`
**Summary:** List gist commits
**Status:** planned

**Operations:**
- **read_one**
  - Component: `commit`
  - Filters:
    - `gist_id` eq `path.gist_id`

#### `GET /repos/{owner}/{repo}/commits`
**Summary:** List commits
**Status:** planned

**Operations:**
- **read_one**
  - Component: `commit`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Query parameters: sha, path, author, committer, since, until

#### `GET /repos/{owner}/{repo}/commits/{ref}`
**Summary:** Get a commit
**Status:** planned

**Operations:**
- **read_one**
  - Component: `commit`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `ref` eq `path.ref`
  - Notes:
    - Response body references #/components/schemas/commit

#### `GET /repos/{owner}/{repo}/pulls/{pull_number}/commits`
**Summary:** List commits on a pull request
**Status:** planned

**Operations:**
- **read_one**
  - Component: `commit`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `pull_number` eq `path.pull_number`

#### `GET /search/commits`
**Summary:** Search commits
**Status:** planned

**Operations:**
- **read_many**
  - Component: `commit`
  - Notes:
    - Query parameters: q, sort

### POST Routes (1)

#### `POST /repos/{owner}/{repo}/merges`
**Summary:** Merge a branch
**Status:** planned

**Operations:**
- **create**
  - Component: `commit`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/commit
