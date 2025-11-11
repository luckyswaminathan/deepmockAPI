# Component Plan: `event`

**API Slug:** `github`
**Total Routes:** 7

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.

## Routes

### GET Routes (7)

#### `GET /events`
**Summary:** List public events
**Status:** planned

**Operations:**
- **read_many**
  - Component: `event`

#### `GET /networks/{owner}/{repo}/events`
**Summary:** List public events for a network of repositories
**Status:** planned

**Operations:**
- **read_one**
  - Component: `event`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`

#### `GET /orgs/{org}/events`
**Summary:** List public organization events
**Status:** planned

**Operations:**
- **read_one**
  - Component: `event`
  - Filters:
    - `org` eq `path.org`

#### `GET /repos/{owner}/{repo}/events`
**Summary:** List repository events
**Status:** planned

**Operations:**
- **read_one**
  - Component: `event`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`

#### `GET /repos/{owner}/{repo}/issues/events`
**Summary:** List issue events for a repository
**Status:** planned

**Operations:**
- **read_one**
  - Component: `event`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`

#### `GET /repos/{owner}/{repo}/issues/{issue_number}/events`
**Summary:** List issue events
**Status:** planned

**Operations:**
- **read_one**
  - Component: `event`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `issue_number` eq `path.issue_number`

#### `GET /users/{username}/events`
**Summary:** List events for the authenticated user
**Status:** planned

**Operations:**
- **read_one**
  - Component: `event`
  - Filters:
    - `username` eq `path.username`
