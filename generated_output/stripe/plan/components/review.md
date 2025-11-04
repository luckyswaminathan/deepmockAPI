# Component Plan: `review`

**API Slug:** `stripe`
**Total Routes:** 3

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.

## Routes

### GET Routes (2)

#### `GET /v1/reviews`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `review`
  - Notes:
    - Query parameters: created, ending_before, expand, limit, starting_after

#### `GET /v1/reviews/{review}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `review`
  - Filters:
    - `review` eq `path.review`
  - Notes:
    - Response body references #/components/schemas/review
    - Query parameters: expand

### POST Routes (1)

#### `POST /v1/reviews/{review}/approve`
**Status:** planned

**Operations:**
- **create**
  - Component: `review`
  - Filters:
    - `review` eq `path.review`
  - Notes:
    - Response body references #/components/schemas/review
    - Query parameters: review
