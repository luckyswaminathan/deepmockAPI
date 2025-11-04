# Component Plan: `identity.verification_report`

**API Slug:** `stripe`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /v1/identity/verification_reports/{report}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `identity.verification_report`
  - Filters:
    - `report` eq `path.report`
  - Notes:
    - Response body references #/components/schemas/identity.verification_report
    - Query parameters: expand
