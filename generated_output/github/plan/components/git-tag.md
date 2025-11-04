# Component Plan: `git-tag`

**API Slug:** `github`
**Total Routes:** 2

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/git/tags/{tag_sha}`
**Summary:** Get a tag
**Status:** planned

**Operations:**
- **read_one**
  - Component: `git-tag`
  - Filters:
    - `tag_sha` eq `path.tag_sha`
  - Notes:
    - Response body references #/components/schemas/git-tag
    - Query parameters: tag_sha

### POST Routes (1)

#### `POST /repos/{owner}/{repo}/git/tags`
**Summary:** Create a tag object
**Status:** planned

**Operations:**
- **create**
  - Component: `git-tag`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/git-tag
