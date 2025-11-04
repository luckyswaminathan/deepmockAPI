# Component Plan: `setup_attempt`

**API Slug:** `stripe`
**Total Routes:** 1

## Supported Operations
- **`read_many`**: List or search records.

## Routes

### GET Routes (1)

#### `GET /v1/setup_attempts`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `setup_attempt`
  - Notes:
    - Query parameters: created, ending_before, expand, limit, setup_intent, starting_after
