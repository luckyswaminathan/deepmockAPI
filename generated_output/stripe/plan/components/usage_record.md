# Component Plan: `usage_record`

**API Slug:** `stripe`
**Total Routes:** 1

## Supported Operations
- **`create`**: Create a new record for the component.

## Routes

### POST Routes (1)

#### `POST /v1/subscription_items/{subscription_item}/usage_records`
**Status:** planned

**Operations:**
- **create**
  - Component: `usage_record`
  - Filters:
    - `subscription_item` eq `path.subscription_item`
  - Notes:
    - Response body references #/components/schemas/usage_record
    - Query parameters: subscription_item
