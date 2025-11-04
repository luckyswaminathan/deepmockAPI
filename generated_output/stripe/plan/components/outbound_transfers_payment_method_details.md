# Component Plan: `outbound_transfers_payment_method_details`

**API Slug:** `stripe`
**Total Routes:** 1

## Supported Operations
- **`read_many`**: List or search records.

## Routes

### GET Routes (1)

#### `GET /v1/treasury/outbound_transfers`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `outbound_transfers_payment_method_details`
  - Notes:
    - Query parameters: ending_before, expand, financial_account, limit, starting_after, status
