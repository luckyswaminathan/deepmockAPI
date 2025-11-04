# Component Plan: `invoiceitem`

**API Slug:** `stripe`
**Total Routes:** 5

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (1)

#### `DELETE /v1/invoiceitems/{invoiceitem}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `invoiceitem`
  - Filters:
    - `invoiceitem` eq `path.invoiceitem`
  - Notes:
    - Query parameters: invoiceitem

### GET Routes (2)

#### `GET /v1/invoiceitems`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `invoiceitem`
  - Notes:
    - Query parameters: created, customer, ending_before, expand, invoice, limit, pending, starting_after

#### `GET /v1/invoiceitems/{invoiceitem}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `invoiceitem`
  - Filters:
    - `invoiceitem` eq `path.invoiceitem`
  - Notes:
    - Response body references #/components/schemas/invoiceitem
    - Query parameters: expand

### POST Routes (2)

#### `POST /v1/invoiceitems`
**Status:** planned

**Operations:**
- **create**
  - Component: `invoiceitem`
  - Notes:
    - Response body references #/components/schemas/invoiceitem

#### `POST /v1/invoiceitems/{invoiceitem}`
**Status:** planned

**Operations:**
- **create**
  - Component: `invoiceitem`
  - Filters:
    - `invoiceitem` eq `path.invoiceitem`
  - Notes:
    - Response body references #/components/schemas/invoiceitem
    - Query parameters: invoiceitem
