# Component Plan: `repository-subscription`

**API Slug:** `github`
**Total Routes:** 2

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.
- **`update`**: Replace a full record.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/subscription`
**Summary:** Get a repository subscription
**Status:** planned

**Operations:**
- **read_one**
  - Component: `repository-subscription`
  - Filters:
    - `owner` eq `path.owner`
    - `repository_url` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/repository-subscription

### PUT Routes (1)

#### `PUT /repos/{owner}/{repo}/subscription`
**Summary:** Set a repository subscription
**Status:** planned

**Operations:**
- **update**
  - Component: `repository-subscription`
  - Filters:
    - `owner` eq `path.owner`
    - `repository_url` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/repository-subscription
