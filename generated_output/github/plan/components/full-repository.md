# Component Plan: `full-repository`

**API Slug:** `github`
**Total Routes:** 7

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`update_partial`**: Apply a partial update to a record.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}`
**Summary:** Get a repository
**Status:** planned

**Operations:**
- **read_one**
  - Component: `full-repository`
  - Filters:
    - `owner` eq `path.owner`
    - `template_repository` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/full-repository

### PATCH Routes (1)

#### `PATCH /repos/{owner}/{repo}`
**Summary:** Update a repository
**Status:** planned

**Operations:**
- **update_partial**
  - Component: `full-repository`
  - Filters:
    - `owner` eq `path.owner`
    - `template_repository` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/full-repository

### POST Routes (5)

#### `POST /orgs/{org}/repos`
**Summary:** Create an organization repository
**Status:** planned

**Operations:**
- **create**
  - Component: `full-repository`
  - Filters:
    - `org` eq `path.org`
  - Notes:
    - Response body references #/components/schemas/full-repository

#### `POST /repos/{owner}/{repo}/forks`
**Summary:** Create a fork
**Status:** planned

**Operations:**
- **create**
  - Component: `full-repository`
  - Filters:
    - `owner` eq `path.owner`
    - `template_repository` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/full-repository

#### `POST /repos/{owner}/{repo}/security-advisories/{ghsa_id}/forks`
**Summary:** Create a temporary private fork
**Status:** planned

**Operations:**
- **create**
  - Component: `full-repository`
  - Filters:
    - `owner` eq `path.owner`
    - `template_repository` eq `path.repo`
    - `ghsa_id` eq `path.ghsa_id`
  - Notes:
    - Response body references #/components/schemas/full-repository

#### `POST /repos/{template_owner}/{template_repo}/generate`
**Summary:** Create a repository using a template
**Status:** planned

**Operations:**
- **create**
  - Component: `full-repository`
  - Filters:
    - `template_owner` eq `path.template_owner`
    - `template_repository` eq `path.template_repo`
  - Notes:
    - Response body references #/components/schemas/full-repository
    - Query parameters: template_owner, template_repo

#### `POST /user/repos`
**Summary:** Create a repository for the authenticated user
**Status:** planned

**Operations:**
- **create**
  - Component: `full-repository`
  - Notes:
    - Response body references #/components/schemas/full-repository
