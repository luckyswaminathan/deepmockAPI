# Component Plan: `issuing.personalization_design`

**API Slug:** `stripe`
**Total Routes:** 6

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /v1/issuing/personalization_designs/{personalization_design}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `issuing.personalization_design`
  - Filters:
    - `personalization_design` eq `path.personalization_design`
  - Notes:
    - Response body references #/components/schemas/issuing.personalization_design
    - Query parameters: expand

### POST Routes (5)

#### `POST /v1/issuing/personalization_designs`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.personalization_design`
  - Notes:
    - Response body references #/components/schemas/issuing.personalization_design

#### `POST /v1/issuing/personalization_designs/{personalization_design}`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.personalization_design`
  - Filters:
    - `personalization_design` eq `path.personalization_design`
  - Notes:
    - Response body references #/components/schemas/issuing.personalization_design
    - Query parameters: personalization_design

#### `POST /v1/test_helpers/issuing/personalization_designs/{personalization_design}/activate`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.personalization_design`
  - Filters:
    - `personalization_design` eq `path.personalization_design`
  - Notes:
    - Response body references #/components/schemas/issuing.personalization_design
    - Query parameters: personalization_design

#### `POST /v1/test_helpers/issuing/personalization_designs/{personalization_design}/deactivate`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.personalization_design`
  - Filters:
    - `personalization_design` eq `path.personalization_design`
  - Notes:
    - Response body references #/components/schemas/issuing.personalization_design
    - Query parameters: personalization_design

#### `POST /v1/test_helpers/issuing/personalization_designs/{personalization_design}/reject`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.personalization_design`
  - Filters:
    - `personalization_design` eq `path.personalization_design`
  - Notes:
    - Response body references #/components/schemas/issuing.personalization_design
    - Query parameters: personalization_design
