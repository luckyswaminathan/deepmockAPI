# Component Plan: `inbound_transfers`

**API Slug:** `stripe`
**Total Routes:** 1

## Supported Operations
- **`read_many`**: List or search records.

## Routes

### GET Routes (1)

#### `GET /v1/treasury/inbound_transfers`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `inbound_transfers`
  - Notes:
    - Query parameters: ending_before, expand, financial_account, limit, starting_after, status
