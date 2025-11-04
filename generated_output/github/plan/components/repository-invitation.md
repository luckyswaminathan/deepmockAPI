# Component Plan: `repository-invitation`

**API Slug:** `github`
**Total Routes:** 2

## Supported Operations
- **`update`**: Replace a full record.
- **`update_partial`**: Apply a partial update to a record.

## Routes

### PATCH Routes (1)

#### `PATCH /repos/{owner}/{repo}/invitations/{invitation_id}`
**Summary:** Update a repository invitation
**Status:** planned

**Operations:**
- **update_partial**
  - Component: `repository-invitation`
  - Filters:
    - `owner` eq `path.owner`
    - `repository` eq `path.repo`
    - `invitation_id` eq `path.invitation_id`
  - Notes:
    - Response body references #/components/schemas/repository-invitation

### PUT Routes (1)

#### `PUT /repos/{owner}/{repo}/collaborators/{username}`
**Summary:** Add a repository collaborator
**Status:** planned

**Operations:**
- **update**
  - Component: `repository-invitation`
  - Filters:
    - `owner` eq `path.owner`
    - `repository` eq `path.repo`
    - `username` eq `path.username`
  - Notes:
    - Response body references #/components/schemas/repository-invitation
