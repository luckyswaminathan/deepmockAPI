# Component Plan: `product_feature`

**API Slug:** `stripe`
**Total Routes:** 2

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /v1/products/{product}/features/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `product_feature`
  - Filters:
    - `id` eq `path.id`
    - `product` eq `path.product`
  - Notes:
    - Response body references #/components/schemas/product_feature
    - Query parameters: expand

### POST Routes (1)

#### `POST /v1/products/{product}/features`
**Status:** planned

**Operations:**
- **create**
  - Component: `product_feature`
  - Filters:
    - `product` eq `path.product`
  - Notes:
    - Response body references #/components/schemas/product_feature
    - Query parameters: product
