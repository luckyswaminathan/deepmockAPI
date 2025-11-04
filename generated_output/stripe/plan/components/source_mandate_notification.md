# Component Plan: `source_mandate_notification`

**API Slug:** `stripe`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /v1/sources/{source}/mandate_notifications/{mandate_notification}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `source_mandate_notification`
  - Filters:
    - `mandate_notification` eq `path.mandate_notification`
    - `source` eq `path.source`
  - Notes:
    - Response body references #/components/schemas/source_mandate_notification
    - Query parameters: expand
