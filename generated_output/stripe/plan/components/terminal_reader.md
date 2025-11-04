# Component Plan: `terminal.reader`

**API Slug:** `stripe`
**Total Routes:** 7

## Supported Operations
- **`create`**: Create a new record for the component.

## Routes

### POST Routes (7)

#### `POST /v1/terminal/readers`
**Status:** planned

**Operations:**
- **create**
  - Component: `terminal.reader`
  - Notes:
    - Response body references #/components/schemas/terminal.reader

#### `POST /v1/terminal/readers/{reader}/cancel_action`
**Status:** planned

**Operations:**
- **create**
  - Component: `terminal.reader`
  - Filters:
    - `reader` eq `path.reader`
  - Notes:
    - Response body references #/components/schemas/terminal.reader
    - Query parameters: reader

#### `POST /v1/terminal/readers/{reader}/process_payment_intent`
**Status:** planned

**Operations:**
- **create**
  - Component: `terminal.reader`
  - Filters:
    - `reader` eq `path.reader`
  - Notes:
    - Response body references #/components/schemas/terminal.reader
    - Query parameters: reader

#### `POST /v1/terminal/readers/{reader}/process_setup_intent`
**Status:** planned

**Operations:**
- **create**
  - Component: `terminal.reader`
  - Filters:
    - `reader` eq `path.reader`
  - Notes:
    - Response body references #/components/schemas/terminal.reader
    - Query parameters: reader

#### `POST /v1/terminal/readers/{reader}/refund_payment`
**Status:** planned

**Operations:**
- **create**
  - Component: `terminal.reader`
  - Filters:
    - `reader` eq `path.reader`
  - Notes:
    - Response body references #/components/schemas/terminal.reader
    - Query parameters: reader

#### `POST /v1/terminal/readers/{reader}/set_reader_display`
**Status:** planned

**Operations:**
- **create**
  - Component: `terminal.reader`
  - Filters:
    - `reader` eq `path.reader`
  - Notes:
    - Response body references #/components/schemas/terminal.reader
    - Query parameters: reader

#### `POST /v1/test_helpers/terminal/readers/{reader}/present_payment_method`
**Status:** planned

**Operations:**
- **create**
  - Component: `terminal.reader`
  - Filters:
    - `reader` eq `path.reader`
  - Notes:
    - Response body references #/components/schemas/terminal.reader
    - Query parameters: reader
