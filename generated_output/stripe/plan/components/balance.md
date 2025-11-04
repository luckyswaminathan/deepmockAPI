# Component Plan: `balance`

**API Slug:** `stripe`
**Total Routes:** 1

## Supported Operations
- **`read_many`**: List or search records.

## Routes

### GET Routes (1)

#### `GET /v1/balance`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `balance`
  - Notes:
    - Response body references #/components/schemas/balance
    - Query parameters: expand
