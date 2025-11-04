# Component Plan: `subscription`

**API Slug:** `stripe`
**Total Routes:** 11

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (2)

#### `DELETE /v1/customers/{customer}/subscriptions/{subscription_exposed_id}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `subscription`
  - Filters:
    - `customer` eq `path.customer`
    - `subscription_exposed_id` eq `path.subscription_exposed_id`
  - Notes:
    - Response body references #/components/schemas/subscription
    - Query parameters: customer, subscription_exposed_id

#### `DELETE /v1/subscriptions/{subscription_exposed_id}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `subscription`
  - Filters:
    - `subscription_exposed_id` eq `path.subscription_exposed_id`
  - Notes:
    - Response body references #/components/schemas/subscription
    - Query parameters: subscription_exposed_id

### GET Routes (4)

#### `GET /v1/customers/{customer}/subscriptions`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `subscription`
  - Filters:
    - `customer` eq `path.customer`
  - Notes:
    - Query parameters: ending_before, expand, limit, starting_after

#### `GET /v1/customers/{customer}/subscriptions/{subscription_exposed_id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `subscription`
  - Filters:
    - `customer` eq `path.customer`
    - `subscription_exposed_id` eq `path.subscription_exposed_id`
  - Notes:
    - Response body references #/components/schemas/subscription
    - Query parameters: expand

#### `GET /v1/subscriptions`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `subscription`
  - Notes:
    - Query parameters: automatic_tax, collection_method, created, current_period_end, current_period_start, customer, ending_before, expand, limit, price, starting_after, status, test_clock

#### `GET /v1/subscriptions/{subscription_exposed_id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `subscription`
  - Filters:
    - `subscription_exposed_id` eq `path.subscription_exposed_id`
  - Notes:
    - Response body references #/components/schemas/subscription
    - Query parameters: expand

### POST Routes (5)

#### `POST /v1/customers/{customer}/subscriptions`
**Status:** planned

**Operations:**
- **create**
  - Component: `subscription`
  - Filters:
    - `customer` eq `path.customer`
  - Notes:
    - Response body references #/components/schemas/subscription
    - Query parameters: customer

#### `POST /v1/customers/{customer}/subscriptions/{subscription_exposed_id}`
**Status:** planned

**Operations:**
- **create**
  - Component: `subscription`
  - Filters:
    - `customer` eq `path.customer`
    - `subscription_exposed_id` eq `path.subscription_exposed_id`
  - Notes:
    - Response body references #/components/schemas/subscription
    - Query parameters: customer, subscription_exposed_id

#### `POST /v1/subscriptions`
**Status:** planned

**Operations:**
- **create**
  - Component: `subscription`
  - Notes:
    - Response body references #/components/schemas/subscription

#### `POST /v1/subscriptions/{subscription_exposed_id}`
**Status:** planned

**Operations:**
- **create**
  - Component: `subscription`
  - Filters:
    - `subscription_exposed_id` eq `path.subscription_exposed_id`
  - Notes:
    - Response body references #/components/schemas/subscription
    - Query parameters: subscription_exposed_id

#### `POST /v1/subscriptions/{subscription}/resume`
**Status:** planned

**Operations:**
- **create**
  - Component: `subscription`
  - Filters:
    - `subscription` eq `path.subscription`
  - Notes:
    - Response body references #/components/schemas/subscription
    - Query parameters: subscription
