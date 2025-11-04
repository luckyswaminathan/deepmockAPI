# Component Plan: `reporting.report_run`

**API Slug:** `stripe`
**Total Routes:** 2

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /v1/reporting/report_runs/{report_run}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `reporting.report_run`
  - Filters:
    - `report_run` eq `path.report_run`
  - Notes:
    - Response body references #/components/schemas/reporting.report_run
    - Query parameters: expand

### POST Routes (1)

#### `POST /v1/reporting/report_runs`
**Status:** planned

**Operations:**
- **create**
  - Component: `reporting.report_run`
  - Notes:
    - Response body references #/components/schemas/reporting.report_run
