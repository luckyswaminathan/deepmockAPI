# Component Plan: `Order`

**API Slug:** `sample_api`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /orders/{orderId}`
**Summary:** Get order
**Status:** planned

**Operations:**
- **read_one**
  - Component: `Order`
  - Filters:
    - `orderId` eq `path.orderId`
  - Notes:
    - Response body references #/components/schemas/Order
    - Query parameters: orderId
