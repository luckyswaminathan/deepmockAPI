# Component Plan: `copilot-seat-details`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /orgs/{org}/members/{username}/copilot`
**Summary:** Get Copilot seat assignment details for a user
**Status:** planned

**Operations:**
- **read_one**
  - Component: `copilot-seat-details`
  - Filters:
    - `org` eq `path.org`
    - `username` eq `path.username`
  - Notes:
    - Response body references #/components/schemas/copilot-seat-details
