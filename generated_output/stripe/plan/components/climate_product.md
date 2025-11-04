# Component Plan: `climate.product`

**API Slug:** `stripe`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /v1/climate/products/{product}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `climate.product`
  - Filters:
    - `product` eq `path.product`
  - Notes:
    - Response body references #/components/schemas/climate.product
    - Query parameters: expand
