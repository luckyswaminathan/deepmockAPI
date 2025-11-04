# Component Plan: `line_item`

**API Slug:** `stripe`
**Total Routes:** 6

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (5)

#### `GET /v1/checkout/sessions/{session}/line_items`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `line_item`
  - Filters:
    - `session` eq `path.session`
  - Notes:
    - Query parameters: ending_before, expand, limit, starting_after

#### `GET /v1/payment_links/{payment_link}/line_items`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `line_item`
  - Filters:
    - `payment_link` eq `path.payment_link`
  - Notes:
    - Query parameters: ending_before, expand, limit, starting_after

#### `GET /v1/quotes/{quote}/line_items`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `line_item`
  - Filters:
    - `quote` eq `path.quote`
  - Notes:
    - Query parameters: ending_before, expand, limit, starting_after

#### `GET /v1/tax/calculations/{calculation}/line_items`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `line_item`
  - Filters:
    - `calculation` eq `path.calculation`
  - Notes:
    - Query parameters: ending_before, expand, limit, starting_after

#### `GET /v1/tax/transactions/{transaction}/line_items`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `line_item`
  - Filters:
    - `transaction` eq `path.transaction`
  - Notes:
    - Query parameters: ending_before, expand, limit, starting_after

### POST Routes (1)

#### `POST /v1/invoices/{invoice}/lines/{line_item_id}`
**Status:** planned

**Operations:**
- **create**
  - Component: `line_item`
  - Filters:
    - `invoice` eq `path.invoice`
    - `line_item_id` eq `path.line_item_id`
  - Notes:
    - Response body references #/components/schemas/line_item
    - Query parameters: invoice, line_item_id
