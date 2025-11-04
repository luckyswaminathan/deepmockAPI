# Component Plan: `authentication-token`

**API Slug:** `github`
**Total Routes:** 4

## Supported Operations
- **`create`**: Create a new record for the component.

## Routes

### POST Routes (4)

#### `POST /orgs/{org}/actions/runners/registration-token`
**Summary:** Create a registration token for an organization
**Status:** planned

**Operations:**
- **create**
  - Component: `authentication-token`
  - Filters:
    - `org` eq `path.org`
  - Notes:
    - Response body references #/components/schemas/authentication-token

#### `POST /orgs/{org}/actions/runners/remove-token`
**Summary:** Create a remove token for an organization
**Status:** planned

**Operations:**
- **create**
  - Component: `authentication-token`
  - Filters:
    - `org` eq `path.org`
  - Notes:
    - Response body references #/components/schemas/authentication-token

#### `POST /repos/{owner}/{repo}/actions/runners/registration-token`
**Summary:** Create a registration token for a repository
**Status:** planned

**Operations:**
- **create**
  - Component: `authentication-token`
  - Filters:
    - `owner` eq `path.owner`
    - `repositories` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/authentication-token

#### `POST /repos/{owner}/{repo}/actions/runners/remove-token`
**Summary:** Create a remove token for a repository
**Status:** planned

**Operations:**
- **create**
  - Component: `authentication-token`
  - Filters:
    - `owner` eq `path.owner`
    - `repositories` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/authentication-token
