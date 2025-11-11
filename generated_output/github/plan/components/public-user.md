# Component Plan: `public-user`

**API Slug:** `github`
**Total Routes:** 3

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.

## Routes

### GET Routes (3)

#### `GET /gists/public`
**Summary:** List public gists
**Status:** planned

**Operations:**
- **read_many**
  - Component: `public-user`

#### `GET /users/{username}/events/public`
**Summary:** List public events for a user
**Status:** planned

**Operations:**
- **read_one**
  - Component: `public-user`
  - Filters:
    - `twitter_username` eq `path.username`

#### `GET /users/{username}/received_events/public`
**Summary:** List public events received by a user
**Status:** planned

**Operations:**
- **read_one**
  - Component: `public-user`
  - Filters:
    - `twitter_username` eq `path.username`
