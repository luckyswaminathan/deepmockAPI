# Component Plan: `git-tree`

**API Slug:** `github`
**Total Routes:** 2

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/git/trees/{tree_sha}`
**Summary:** Get a tree
**Status:** planned

**Operations:**
- **read_one**
  - Component: `git-tree`
  - Filters:
    - `tree_sha` eq `path.tree_sha`
  - Notes:
    - Response body references #/components/schemas/git-tree
    - Query parameters: recursive

### POST Routes (1)

#### `POST /repos/{owner}/{repo}/git/trees`
**Summary:** Create a tree
**Status:** planned

**Operations:**
- **create**
  - Component: `git-tree`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/git-tree
