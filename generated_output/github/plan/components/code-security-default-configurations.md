# Component Plan: `code-security-default-configurations`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /orgs/{org}/code-security/configurations/defaults`
**Summary:** Get default code security configurations
**Status:** planned

**Operations:**
- **read_one**
  - Component: `code-security-default-configurations`
  - Filters:
    - `org` eq `path.org`
  - Notes:
    - Response body references #/components/schemas/code-security-default-configurations
