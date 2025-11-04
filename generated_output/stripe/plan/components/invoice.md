# Component Plan: `invoice`

**API Slug:** `stripe`
**Total Routes:** 15

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (1)

#### `DELETE /v1/invoices/{invoice}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `invoice`
  - Filters:
    - `from_invoice` eq `path.invoice`
  - Notes:
    - Query parameters: invoice

### GET Routes (3)

#### `GET /v1/invoices`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `invoice`
  - Notes:
    - Query parameters: collection_method, created, customer, due_date, ending_before, expand, limit, starting_after, status, subscription

#### `GET /v1/invoices/upcoming`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `invoice`
  - Notes:
    - Response body references #/components/schemas/invoice
    - Query parameters: automatic_tax, coupon, currency, customer, customer_details, discounts, expand, invoice_items, issuer, on_behalf_of, preview_mode, schedule, schedule_details, subscription, subscription_billing_cycle_anchor, subscription_cancel_at, subscription_cancel_at_period_end, subscription_cancel_now, subscription_default_tax_rates, subscription_details, subscription_items, subscription_proration_behavior, subscription_proration_date, subscription_resume_at, subscription_start_date, subscription_trial_end

#### `GET /v1/invoices/{invoice}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `invoice`
  - Filters:
    - `from_invoice` eq `path.invoice`
  - Notes:
    - Response body references #/components/schemas/invoice
    - Query parameters: expand

### POST Routes (11)

#### `POST /v1/invoices`
**Status:** planned

**Operations:**
- **create**
  - Component: `invoice`
  - Notes:
    - Response body references #/components/schemas/invoice

#### `POST /v1/invoices/create_preview`
**Status:** planned

**Operations:**
- **create**
  - Component: `invoice`
  - Notes:
    - Response body references #/components/schemas/invoice

#### `POST /v1/invoices/{invoice}`
**Status:** planned

**Operations:**
- **create**
  - Component: `invoice`
  - Filters:
    - `from_invoice` eq `path.invoice`
  - Notes:
    - Response body references #/components/schemas/invoice
    - Query parameters: invoice

#### `POST /v1/invoices/{invoice}/add_lines`
**Status:** planned

**Operations:**
- **create**
  - Component: `invoice`
  - Filters:
    - `from_invoice` eq `path.invoice`
  - Notes:
    - Response body references #/components/schemas/invoice
    - Query parameters: invoice

#### `POST /v1/invoices/{invoice}/finalize`
**Status:** planned

**Operations:**
- **create**
  - Component: `invoice`
  - Filters:
    - `from_invoice` eq `path.invoice`
  - Notes:
    - Response body references #/components/schemas/invoice
    - Query parameters: invoice

#### `POST /v1/invoices/{invoice}/mark_uncollectible`
**Status:** planned

**Operations:**
- **create**
  - Component: `invoice`
  - Filters:
    - `from_invoice` eq `path.invoice`
  - Notes:
    - Response body references #/components/schemas/invoice
    - Query parameters: invoice

#### `POST /v1/invoices/{invoice}/pay`
**Status:** planned

**Operations:**
- **create**
  - Component: `invoice`
  - Filters:
    - `from_invoice` eq `path.invoice`
  - Notes:
    - Response body references #/components/schemas/invoice
    - Query parameters: invoice

#### `POST /v1/invoices/{invoice}/remove_lines`
**Status:** planned

**Operations:**
- **create**
  - Component: `invoice`
  - Filters:
    - `from_invoice` eq `path.invoice`
  - Notes:
    - Response body references #/components/schemas/invoice
    - Query parameters: invoice

#### `POST /v1/invoices/{invoice}/send`
**Status:** planned

**Operations:**
- **create**
  - Component: `invoice`
  - Filters:
    - `from_invoice` eq `path.invoice`
  - Notes:
    - Response body references #/components/schemas/invoice
    - Query parameters: invoice

#### `POST /v1/invoices/{invoice}/update_lines`
**Status:** planned

**Operations:**
- **create**
  - Component: `invoice`
  - Filters:
    - `from_invoice` eq `path.invoice`
  - Notes:
    - Response body references #/components/schemas/invoice
    - Query parameters: invoice

#### `POST /v1/invoices/{invoice}/void`
**Status:** planned

**Operations:**
- **create**
  - Component: `invoice`
  - Filters:
    - `from_invoice` eq `path.invoice`
  - Notes:
    - Response body references #/components/schemas/invoice
    - Query parameters: invoice
