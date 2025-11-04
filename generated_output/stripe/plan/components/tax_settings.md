# Component Plan: `tax.settings`

**API Slug:** `stripe`
**Total Routes:** 2

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_many`**: List or search records.

## Routes

### GET Routes (1)

#### `GET /v1/tax/settings`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `tax.settings`
  - Notes:
    - Response body references #/components/schemas/tax.settings
    - Query parameters: expand

### POST Routes (1)

#### `POST /v1/tax/settings`
**Status:** planned

**Operations:**
- **create**
  - Component: `tax.settings`
  - Notes:
    - Response body references #/components/schemas/tax.settings
