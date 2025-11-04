# Component Plan: `funding_instructions`

**API Slug:** `stripe`
**Total Routes:** 1

## Supported Operations
- **`create`**: Create a new record for the component.

## Routes

### POST Routes (1)

#### `POST /v1/customers/{customer}/funding_instructions`
**Status:** planned

**Operations:**
- **create**
  - Component: `funding_instructions`
  - Filters:
    - `customer` eq `path.customer`
  - Notes:
    - Response body references #/components/schemas/funding_instructions
    - Query parameters: customer
