# Component Plan: `entitlements.active_entitlement`

**API Slug:** `stripe`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /v1/entitlements/active_entitlements/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `entitlements.active_entitlement`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/entitlements.active_entitlement
    - Query parameters: expand
