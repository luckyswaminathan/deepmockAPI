# Component Plan: `discount`

**API Slug:** `stripe`
**Total Routes:** 5

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (3)

#### `DELETE /v1/customers/{customer}/discount`
**Status:** planned

**Operations:**
- **delete**
  - Component: `discount`
  - Filters:
    - `customer` eq `path.customer`
  - Notes:
    - Query parameters: customer

#### `DELETE /v1/customers/{customer}/subscriptions/{subscription_exposed_id}/discount`
**Status:** planned

**Operations:**
- **delete**
  - Component: `discount`
  - Filters:
    - `customer` eq `path.customer`
    - `subscription_exposed_id` eq `path.subscription_exposed_id`
  - Notes:
    - Query parameters: customer, subscription_exposed_id

#### `DELETE /v1/subscriptions/{subscription_exposed_id}/discount`
**Status:** planned

**Operations:**
- **delete**
  - Component: `discount`
  - Filters:
    - `subscription_exposed_id` eq `path.subscription_exposed_id`
  - Notes:
    - Query parameters: subscription_exposed_id

### GET Routes (2)

#### `GET /v1/customers/{customer}/discount`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `discount`
  - Filters:
    - `customer` eq `path.customer`
  - Notes:
    - Response body references #/components/schemas/discount
    - Query parameters: expand

#### `GET /v1/customers/{customer}/subscriptions/{subscription_exposed_id}/discount`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `discount`
  - Filters:
    - `customer` eq `path.customer`
    - `subscription_exposed_id` eq `path.subscription_exposed_id`
  - Notes:
    - Response body references #/components/schemas/discount
    - Query parameters: expand
