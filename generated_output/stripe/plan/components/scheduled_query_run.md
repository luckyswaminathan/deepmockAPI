# Component Plan: `scheduled_query_run`

**API Slug:** `stripe`
**Total Routes:** 2

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.

## Routes

### GET Routes (2)

#### `GET /v1/sigma/scheduled_query_runs`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `scheduled_query_run`
  - Notes:
    - Query parameters: ending_before, expand, limit, starting_after

#### `GET /v1/sigma/scheduled_query_runs/{scheduled_query_run}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `scheduled_query_run`
  - Filters:
    - `scheduled_query_run` eq `path.scheduled_query_run`
  - Notes:
    - Response body references #/components/schemas/scheduled_query_run
    - Query parameters: expand
