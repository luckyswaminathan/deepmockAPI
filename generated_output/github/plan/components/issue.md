# Component Plan: `issue`

**API Slug:** `github`
**Total Routes:** 10

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.
- **`update_partial`**: Apply a partial update to a record.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (1)

#### `DELETE /repos/{owner}/{repo}/issues/{issue_number}/assignees`
**Summary:** Remove assignees from an issue
**Status:** planned

**Operations:**
- **delete**
  - Component: `issue`
  - Filters:
    - `owner` eq `path.owner`
    - `repository_url` eq `path.repo`
    - `issue_number` eq `path.issue_number`
  - Notes:
    - Response body references #/components/schemas/issue

### GET Routes (6)

#### `GET /issues`
**Summary:** List issues assigned to the authenticated user
**Status:** planned

**Operations:**
- **read_many**
  - Component: `issue`
  - Notes:
    - Query parameters: filter, state, sort, collab, orgs, owned, pulls

#### `GET /orgs/{org}/issues`
**Summary:** List organization issues assigned to the authenticated user
**Status:** planned

**Operations:**
- **read_one**
  - Component: `issue`
  - Filters:
    - `org` eq `path.org`
  - Notes:
    - Query parameters: filter, state, sort

#### `GET /repos/{owner}/{repo}/issues`
**Summary:** List repository issues
**Status:** planned

**Operations:**
- **read_one**
  - Component: `issue`
  - Filters:
    - `owner` eq `path.owner`
    - `repository_url` eq `path.repo`
  - Notes:
    - Query parameters: milestone, state, assignee, creator, mentioned, sort

#### `GET /repos/{owner}/{repo}/issues/{issue_number}`
**Summary:** Get an issue
**Status:** planned

**Operations:**
- **read_one**
  - Component: `issue`
  - Filters:
    - `owner` eq `path.owner`
    - `repository_url` eq `path.repo`
    - `issue_number` eq `path.issue_number`
  - Notes:
    - Response body references #/components/schemas/issue

#### `GET /search/issues`
**Summary:** Search issues and pull requests
**Status:** planned

**Operations:**
- **read_many**
  - Component: `issue`
  - Notes:
    - Query parameters: q, sort

#### `GET /user/issues`
**Summary:** List user account issues assigned to the authenticated user
**Status:** planned

**Operations:**
- **read_many**
  - Component: `issue`
  - Notes:
    - Query parameters: filter, state, sort

### PATCH Routes (1)

#### `PATCH /repos/{owner}/{repo}/issues/{issue_number}`
**Summary:** Update an issue
**Status:** planned

**Operations:**
- **update_partial**
  - Component: `issue`
  - Filters:
    - `owner` eq `path.owner`
    - `repository_url` eq `path.repo`
    - `issue_number` eq `path.issue_number`
  - Notes:
    - Response body references #/components/schemas/issue

### POST Routes (2)

#### `POST /repos/{owner}/{repo}/issues`
**Summary:** Create an issue
**Status:** planned

**Operations:**
- **create**
  - Component: `issue`
  - Filters:
    - `owner` eq `path.owner`
    - `repository_url` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/issue

#### `POST /repos/{owner}/{repo}/issues/{issue_number}/assignees`
**Summary:** Add assignees to an issue
**Status:** planned

**Operations:**
- **create**
  - Component: `issue`
  - Filters:
    - `owner` eq `path.owner`
    - `repository_url` eq `path.repo`
    - `issue_number` eq `path.issue_number`
  - Notes:
    - Response body references #/components/schemas/issue
