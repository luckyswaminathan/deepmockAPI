# Component Plan: `dependabot-public-key`

**API Slug:** `github`
**Total Routes:** 2

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (2)

#### `GET /orgs/{org}/dependabot/secrets/public-key`
**Summary:** Get an organization public key
**Status:** planned

**Operations:**
- **read_one**
  - Component: `dependabot-public-key`
  - Filters:
    - `org` eq `path.org`
  - Notes:
    - Response body references #/components/schemas/dependabot-public-key

#### `GET /repos/{owner}/{repo}/dependabot/secrets/public-key`
**Summary:** Get a repository public key
**Status:** planned

**Operations:**
- **read_one**
  - Component: `dependabot-public-key`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/dependabot-public-key
