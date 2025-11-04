# Component Plan: `codespace`

**API Slug:** `github`
**Total Routes:** 14

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.
- **`update_partial`**: Apply a partial update to a record.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (2)

#### `DELETE /orgs/{org}/members/{username}/codespaces/{codespace_name}`
**Summary:** Delete a codespace from the organization
**Status:** planned

**Operations:**
- **delete**
  - Component: `codespace`
  - Filters:
    - `org` eq `path.org`
    - `username` eq `path.username`
    - `codespace_name` eq `path.codespace_name`

#### `DELETE /user/codespaces/{codespace_name}`
**Summary:** Delete a codespace for the authenticated user
**Status:** planned

**Operations:**
- **delete**
  - Component: `codespace`
  - Filters:
    - `codespace_name` eq `path.codespace_name`

### GET Routes (5)

#### `GET /orgs/{org}/codespaces`
**Summary:** List codespaces for the organization
**Status:** planned

**Operations:**
- **read_one**
  - Component: `codespace`
  - Filters:
    - `org` eq `path.org`

#### `GET /orgs/{org}/members/{username}/codespaces`
**Summary:** List codespaces for a user in organization
**Status:** planned

**Operations:**
- **read_one**
  - Component: `codespace`
  - Filters:
    - `org` eq `path.org`
    - `username` eq `path.username`

#### `GET /repos/{owner}/{repo}/codespaces`
**Summary:** List codespaces in a repository for the authenticated user
**Status:** planned

**Operations:**
- **read_one**
  - Component: `codespace`
  - Filters:
    - `owner` eq `path.owner`
    - `repository` eq `path.repo`

#### `GET /user/codespaces`
**Summary:** List codespaces for the authenticated user
**Status:** planned

**Operations:**
- **read_many**
  - Component: `codespace`

#### `GET /user/codespaces/{codespace_name}`
**Summary:** Get a codespace for the authenticated user
**Status:** planned

**Operations:**
- **read_one**
  - Component: `codespace`
  - Filters:
    - `codespace_name` eq `path.codespace_name`
  - Notes:
    - Response body references #/components/schemas/codespace

### PATCH Routes (1)

#### `PATCH /user/codespaces/{codespace_name}`
**Summary:** Update a codespace for the authenticated user
**Status:** planned

**Operations:**
- **update_partial**
  - Component: `codespace`
  - Filters:
    - `codespace_name` eq `path.codespace_name`
  - Notes:
    - Response body references #/components/schemas/codespace

### POST Routes (6)

#### `POST /orgs/{org}/members/{username}/codespaces/{codespace_name}/stop`
**Summary:** Stop a codespace for an organization user
**Status:** planned

**Operations:**
- **create**
  - Component: `codespace`
  - Filters:
    - `org` eq `path.org`
    - `username` eq `path.username`
    - `codespace_name` eq `path.codespace_name`
  - Notes:
    - Response body references #/components/schemas/codespace

#### `POST /repos/{owner}/{repo}/codespaces`
**Summary:** Create a codespace in a repository
**Status:** planned

**Operations:**
- **create**
  - Component: `codespace`
  - Filters:
    - `owner` eq `path.owner`
    - `repository` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/codespace

#### `POST /repos/{owner}/{repo}/pulls/{pull_number}/codespaces`
**Summary:** Create a codespace from a pull request
**Status:** planned

**Operations:**
- **create**
  - Component: `codespace`
  - Filters:
    - `owner` eq `path.owner`
    - `repository` eq `path.repo`
    - `pull_number` eq `path.pull_number`
  - Notes:
    - Response body references #/components/schemas/codespace

#### `POST /user/codespaces`
**Summary:** Create a codespace for the authenticated user
**Status:** planned

**Operations:**
- **create**
  - Component: `codespace`
  - Notes:
    - Response body references #/components/schemas/codespace

#### `POST /user/codespaces/{codespace_name}/start`
**Summary:** Start a codespace for the authenticated user
**Status:** planned

**Operations:**
- **create**
  - Component: `codespace`
  - Filters:
    - `codespace_name` eq `path.codespace_name`
  - Notes:
    - Response body references #/components/schemas/codespace

#### `POST /user/codespaces/{codespace_name}/stop`
**Summary:** Stop a codespace for the authenticated user
**Status:** planned

**Operations:**
- **create**
  - Component: `codespace`
  - Filters:
    - `codespace_name` eq `path.codespace_name`
  - Notes:
    - Response body references #/components/schemas/codespace
