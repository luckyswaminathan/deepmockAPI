# Component Plan: `integration`

**API Slug:** `github`
**Total Routes:** 2

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.

## Routes

### GET Routes (2)

#### `GET /app`
**Summary:** Get the authenticated app
**Status:** planned

**Operations:**
- **read_many**
  - Component: `integration`
  - Notes:
    - Response body references #/components/schemas/integration

#### `GET /apps/{app_slug}`
**Summary:** Get an app
**Status:** planned

**Operations:**
- **read_one**
  - Component: `integration`
  - Filters:
    - `app_slug` eq `path.app_slug`
  - Notes:
    - Response body references #/components/schemas/integration
