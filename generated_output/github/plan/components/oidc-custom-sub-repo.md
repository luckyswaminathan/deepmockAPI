# Component Plan: `oidc-custom-sub-repo`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/actions/oidc/customization/sub`
**Summary:** Get the customization template for an OIDC subject claim for a repository
**Status:** planned

**Operations:**
- **read_one**
  - Component: `oidc-custom-sub-repo`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/oidc-custom-sub-repo
