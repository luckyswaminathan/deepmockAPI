# Component Plan: `git-commit`

**API Slug:** `github`
**Total Routes:** 2

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/git/commits/{commit_sha}`
**Summary:** Get a commit object
**Status:** planned

**Operations:**
- **read_one**
  - Component: `git-commit`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `commit_sha` eq `path.commit_sha`
  - Notes:
    - Response body references #/components/schemas/git-commit

### POST Routes (1)

#### `POST /repos/{owner}/{repo}/git/commits`
**Summary:** Create a commit
**Status:** planned

**Operations:**
- **create**
  - Component: `git-commit`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/git-commit
