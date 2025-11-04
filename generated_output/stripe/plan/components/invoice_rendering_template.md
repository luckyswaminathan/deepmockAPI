# Component Plan: `invoice_rendering_template`

**API Slug:** `stripe`
**Total Routes:** 4

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.

## Routes

### GET Routes (2)

#### `GET /v1/invoice_rendering_templates`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `invoice_rendering_template`
  - Notes:
    - Query parameters: ending_before, expand, limit, starting_after, status

#### `GET /v1/invoice_rendering_templates/{template}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `invoice_rendering_template`
  - Filters:
    - `template` eq `path.template`
  - Notes:
    - Response body references #/components/schemas/invoice_rendering_template
    - Query parameters: expand, version

### POST Routes (2)

#### `POST /v1/invoice_rendering_templates/{template}/archive`
**Status:** planned

**Operations:**
- **create**
  - Component: `invoice_rendering_template`
  - Filters:
    - `template` eq `path.template`
  - Notes:
    - Response body references #/components/schemas/invoice_rendering_template
    - Query parameters: template

#### `POST /v1/invoice_rendering_templates/{template}/unarchive`
**Status:** planned

**Operations:**
- **create**
  - Component: `invoice_rendering_template`
  - Filters:
    - `template` eq `path.template`
  - Notes:
    - Response body references #/components/schemas/invoice_rendering_template
    - Query parameters: template
