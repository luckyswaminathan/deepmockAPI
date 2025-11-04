# Component Plan: `autolink`

**API Slug:** `github`
**Total Routes:** 4

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (1)

#### `DELETE /repos/{owner}/{repo}/autolinks/{autolink_id}`
**Summary:** Delete an autolink reference from a repository
**Status:** planned

**Operations:**
- **delete**
  - Component: `autolink`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `autolink_id` eq `path.autolink_id`

### GET Routes (2)

#### `GET /repos/{owner}/{repo}/autolinks`
**Summary:** Get all autolinks of a repository
**Status:** planned

**Operations:**
- **read_one**
  - Component: `autolink`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`

#### `GET /repos/{owner}/{repo}/autolinks/{autolink_id}`
**Summary:** Get an autolink reference of a repository
**Status:** planned

**Operations:**
- **read_one**
  - Component: `autolink`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `autolink_id` eq `path.autolink_id`
  - Notes:
    - Response body references #/components/schemas/autolink

### POST Routes (1)

#### `POST /repos/{owner}/{repo}/autolinks`
**Summary:** Create an autolink reference for a repository
**Status:** planned

**Operations:**
- **create**
  - Component: `autolink`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/autolink
