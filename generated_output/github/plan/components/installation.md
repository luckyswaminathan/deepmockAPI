# Component Plan: `installation`

**API Slug:** `github`
**Total Routes:** 8

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (1)

#### `DELETE /app/installations/{installation_id}`
**Summary:** Delete an installation for the authenticated app
**Status:** planned

**Operations:**
- **delete**
  - Component: `installation`
  - Filters:
    - `installation_id` eq `path.installation_id`

### GET Routes (7)

#### `GET /app/installations`
**Summary:** List installations for the authenticated app
**Status:** planned

**Operations:**
- **read_many**
  - Component: `installation`
  - Notes:
    - Query parameters: outdated

#### `GET /app/installations/{installation_id}`
**Summary:** Get an installation for the authenticated app
**Status:** planned

**Operations:**
- **read_one**
  - Component: `installation`
  - Filters:
    - `installation_id` eq `path.installation_id`
  - Notes:
    - Response body references #/components/schemas/installation

#### `GET /orgs/{org}/installation`
**Summary:** Get an organization installation for the authenticated app
**Status:** planned

**Operations:**
- **read_one**
  - Component: `installation`
  - Filters:
    - `org` eq `path.org`
  - Notes:
    - Response body references #/components/schemas/installation

#### `GET /orgs/{org}/installations`
**Summary:** List app installations for an organization
**Status:** planned

**Operations:**
- **read_one**
  - Component: `installation`
  - Filters:
    - `org` eq `path.org`

#### `GET /repos/{owner}/{repo}/installation`
**Summary:** Get a repository installation for the authenticated app
**Status:** planned

**Operations:**
- **read_one**
  - Component: `installation`
  - Filters:
    - `owner` eq `path.owner`
    - `repository_selection` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/installation

#### `GET /user/installations`
**Summary:** List app installations accessible to the user access token
**Status:** planned

**Operations:**
- **read_many**
  - Component: `installation`

#### `GET /users/{username}/installation`
**Summary:** Get a user installation for the authenticated app
**Status:** planned

**Operations:**
- **read_one**
  - Component: `installation`
  - Filters:
    - `username` eq `path.username`
  - Notes:
    - Response body references #/components/schemas/installation
