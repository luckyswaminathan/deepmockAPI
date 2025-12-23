# Component Plan: `OrderList`

**API Slug:** `sample_api`
**Total Routes:** 1

## Supported Operations
- **`read_many`**: List or search records.

## Routes

### GET Routes (1)

#### `GET /orders`
**Summary:** List orders
**Status:** planned

**Operations:**
- **read_many**
  - Component: `OrderList`
  - Notes:
    - Response body references #/components/schemas/OrderList
