# Component Plan: `interaction-limit`

**API Slug:** `github`
**Total Routes:** 9

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.
- **`update`**: Replace a full record.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (3)

#### `DELETE /orgs/{org}/interaction-limits`
**Summary:** Remove interaction restrictions for an organization
**Status:** planned

**Operations:**
- **delete**
  - Component: `interaction-limit`
  - Filters:
    - `org` eq `path.org`

#### `DELETE /repos/{owner}/{repo}/interaction-limits`
**Summary:** Remove interaction restrictions for a repository
**Status:** planned

**Operations:**
- **delete**
  - Component: `interaction-limit`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`

#### `DELETE /user/interaction-limits`
**Summary:** Remove interaction restrictions from your public repositories
**Status:** planned

**Operations:**
- **delete**
  - Component: `interaction-limit`

### GET Routes (3)

#### `GET /orgs/{org}/interaction-limits`
**Summary:** Get interaction restrictions for an organization
**Status:** planned

**Operations:**
- **read_one**
  - Component: `interaction-limit`
  - Filters:
    - `org` eq `path.org`

#### `GET /repos/{owner}/{repo}/interaction-limits`
**Summary:** Get interaction restrictions for a repository
**Status:** planned

**Operations:**
- **read_one**
  - Component: `interaction-limit`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`

#### `GET /user/interaction-limits`
**Summary:** Get interaction restrictions for your public repositories
**Status:** planned

**Operations:**
- **read_many**
  - Component: `interaction-limit`

### PUT Routes (3)

#### `PUT /orgs/{org}/interaction-limits`
**Summary:** Set interaction restrictions for an organization
**Status:** planned

**Operations:**
- **update**
  - Component: `interaction-limit`
  - Filters:
    - `org` eq `path.org`
  - Notes:
    - Request body references #/components/schemas/interaction-limit
    - Response body references #/components/schemas/interaction-limit-response

#### `PUT /repos/{owner}/{repo}/interaction-limits`
**Summary:** Set interaction restrictions for a repository
**Status:** planned

**Operations:**
- **update**
  - Component: `interaction-limit`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Request body references #/components/schemas/interaction-limit
    - Response body references #/components/schemas/interaction-limit-response

#### `PUT /user/interaction-limits`
**Summary:** Set interaction restrictions for your public repositories
**Status:** planned

**Operations:**
- **update**
  - Component: `interaction-limit`
  - Notes:
    - Request body references #/components/schemas/interaction-limit
    - Response body references #/components/schemas/interaction-limit-response
