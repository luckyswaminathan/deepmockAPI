# Component Plan: `subscription_schedule`

**API Slug:** `stripe`
**Total Routes:** 6

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.

## Routes

### GET Routes (2)

#### `GET /v1/subscription_schedules`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `subscription_schedule`
  - Notes:
    - Query parameters: canceled_at, completed_at, created, customer, ending_before, expand, limit, released_at, scheduled, starting_after

#### `GET /v1/subscription_schedules/{schedule}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `subscription_schedule`
  - Filters:
    - `schedule` eq `path.schedule`
  - Notes:
    - Response body references #/components/schemas/subscription_schedule
    - Query parameters: expand

### POST Routes (4)

#### `POST /v1/subscription_schedules`
**Status:** planned

**Operations:**
- **create**
  - Component: `subscription_schedule`
  - Notes:
    - Response body references #/components/schemas/subscription_schedule

#### `POST /v1/subscription_schedules/{schedule}`
**Status:** planned

**Operations:**
- **create**
  - Component: `subscription_schedule`
  - Filters:
    - `schedule` eq `path.schedule`
  - Notes:
    - Response body references #/components/schemas/subscription_schedule
    - Query parameters: schedule

#### `POST /v1/subscription_schedules/{schedule}/cancel`
**Status:** planned

**Operations:**
- **create**
  - Component: `subscription_schedule`
  - Filters:
    - `schedule` eq `path.schedule`
  - Notes:
    - Response body references #/components/schemas/subscription_schedule
    - Query parameters: schedule

#### `POST /v1/subscription_schedules/{schedule}/release`
**Status:** planned

**Operations:**
- **create**
  - Component: `subscription_schedule`
  - Filters:
    - `schedule` eq `path.schedule`
  - Notes:
    - Response body references #/components/schemas/subscription_schedule
    - Query parameters: schedule
