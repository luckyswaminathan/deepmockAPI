# Component Plan: `copilot-organization-details`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /orgs/{org}/copilot/billing`
**Summary:** Get Copilot seat information and settings for an organization
**Status:** planned

**Operations:**
- **read_one**
  - Component: `copilot-organization-details`
  - Filters:
    - `org` eq `path.org`
  - Notes:
    - Response body references #/components/schemas/copilot-organization-details
