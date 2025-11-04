# Component Plan: `private-user`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`update_partial`**: Apply a partial update to a record.

## Routes

### PATCH Routes (1)

#### `PATCH /user`
**Summary:** Update the authenticated user
**Status:** planned

**Operations:**
- **update_partial**
  - Component: `private-user`
  - Notes:
    - Response body references #/components/schemas/private-user
