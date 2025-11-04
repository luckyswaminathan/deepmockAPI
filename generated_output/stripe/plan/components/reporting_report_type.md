# Component Plan: `reporting.report_type`

**API Slug:** `stripe`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /v1/reporting/report_types/{report_type}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `reporting.report_type`
  - Filters:
    - `report_type` eq `path.report_type`
  - Notes:
    - Response body references #/components/schemas/reporting.report_type
    - Query parameters: expand
