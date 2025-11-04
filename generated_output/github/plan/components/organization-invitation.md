# Component Plan: `organization-invitation`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`create`**: Create a new record for the component.

## Routes

### POST Routes (1)

#### `POST /orgs/{org}/invitations`
**Summary:** Create an organization invitation
**Status:** planned

**Operations:**
- **create**
  - Component: `organization-invitation`
  - Filters:
    - `org` eq `path.org`
  - Notes:
    - Response body references #/components/schemas/organization-invitation
