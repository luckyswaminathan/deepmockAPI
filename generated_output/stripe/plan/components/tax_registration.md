# Component Plan: `tax.registration`

**API Slug:** `stripe`
**Total Routes:** 3

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /v1/tax/registrations/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `tax.registration`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/tax.registration
    - Query parameters: expand

### POST Routes (2)

#### `POST /v1/tax/registrations`
**Status:** planned

**Operations:**
- **create**
  - Component: `tax.registration`
  - Notes:
    - Response body references #/components/schemas/tax.registration

#### `POST /v1/tax/registrations/{id}`
**Status:** planned

**Operations:**
- **create**
  - Component: `tax.registration`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/tax.registration
    - Query parameters: id
