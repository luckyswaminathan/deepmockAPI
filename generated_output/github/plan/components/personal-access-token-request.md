# Component Plan: `personal-access-token-request`

**API Slug:** `github`
**Total Routes:** 3

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /orgs/{org}/personal-access-token-requests`
**Summary:** List requests to access organization resources with fine-grained personal access tokens
**Status:** planned

**Operations:**
- **read_one**
  - Component: `personal-access-token-request`
  - Filters:
    - `org` eq `path.org`

### POST Routes (2)

#### `POST /orgs/{org}/personal-access-token-requests`
**Summary:** Review requests to access organization resources with fine-grained personal access tokens
**Status:** planned

**Operations:**
- **create**
  - Component: `personal-access-token-request`
  - Filters:
    - `org` eq `path.org`

#### `POST /orgs/{org}/personal-access-token-requests/{pat_request_id}`
**Summary:** Review a request to access organization resources with a fine-grained personal access token
**Status:** planned

**Operations:**
- **create**
  - Component: `personal-access-token-request`
  - Filters:
    - `pat_request_id` eq `path.pat_request_id`
  - Notes:
    - Query parameters: pat_request_id
