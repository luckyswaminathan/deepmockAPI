# Component Plan: `credit_note`

**API Slug:** `stripe`
**Total Routes:** 6

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.

## Routes

### GET Routes (3)

#### `GET /v1/credit_notes`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `credit_note`
  - Notes:
    - Query parameters: created, customer, ending_before, expand, invoice, limit, starting_after

#### `GET /v1/credit_notes/preview`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `credit_note`
  - Notes:
    - Response body references #/components/schemas/credit_note
    - Query parameters: amount, credit_amount, effective_at, email_type, expand, invoice, lines, memo, metadata, out_of_band_amount, reason, refund, refund_amount, shipping_cost

#### `GET /v1/credit_notes/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `credit_note`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/credit_note
    - Query parameters: expand

### POST Routes (3)

#### `POST /v1/credit_notes`
**Status:** planned

**Operations:**
- **create**
  - Component: `credit_note`
  - Notes:
    - Response body references #/components/schemas/credit_note

#### `POST /v1/credit_notes/{id}`
**Status:** planned

**Operations:**
- **create**
  - Component: `credit_note`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/credit_note
    - Query parameters: id

#### `POST /v1/credit_notes/{id}/void`
**Status:** planned

**Operations:**
- **create**
  - Component: `credit_note`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/credit_note
    - Query parameters: id
