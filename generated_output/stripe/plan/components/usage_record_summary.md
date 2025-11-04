# Component Plan: `usage_record_summary`

**API Slug:** `stripe`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /v1/subscription_items/{subscription_item}/usage_record_summaries`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `usage_record_summary`
  - Filters:
    - `subscription_item` eq `path.subscription_item`
  - Notes:
    - Query parameters: ending_before, expand, limit, starting_after
