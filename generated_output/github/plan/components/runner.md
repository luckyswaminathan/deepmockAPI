# Component Plan: `runner`

**API Slug:** `github`
**Total Routes:** 6

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (2)

#### `DELETE /orgs/{org}/actions/runners/{runner_id}`
**Summary:** Delete a self-hosted runner from an organization
**Status:** planned

**Operations:**
- **delete**
  - Component: `runner`
  - Filters:
    - `org` eq `path.org`
    - `runner_id` eq `path.runner_id`

#### `DELETE /repos/{owner}/{repo}/actions/runners/{runner_id}`
**Summary:** Delete a self-hosted runner from a repository
**Status:** planned

**Operations:**
- **delete**
  - Component: `runner`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `runner_id` eq `path.runner_id`

### GET Routes (4)

#### `GET /orgs/{org}/actions/runners`
**Summary:** List self-hosted runners for an organization
**Status:** planned

**Operations:**
- **read_one**
  - Component: `runner`
  - Filters:
    - `org` eq `path.org`
  - Notes:
    - Query parameters: name

#### `GET /orgs/{org}/actions/runners/{runner_id}`
**Summary:** Get a self-hosted runner for an organization
**Status:** planned

**Operations:**
- **read_one**
  - Component: `runner`
  - Filters:
    - `org` eq `path.org`
    - `runner_id` eq `path.runner_id`
  - Notes:
    - Response body references #/components/schemas/runner

#### `GET /repos/{owner}/{repo}/actions/runners`
**Summary:** List self-hosted runners for a repository
**Status:** planned

**Operations:**
- **read_one**
  - Component: `runner`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Query parameters: name

#### `GET /repos/{owner}/{repo}/actions/runners/{runner_id}`
**Summary:** Get a self-hosted runner for a repository
**Status:** planned

**Operations:**
- **read_one**
  - Component: `runner`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `runner_id` eq `path.runner_id`
  - Notes:
    - Response body references #/components/schemas/runner
