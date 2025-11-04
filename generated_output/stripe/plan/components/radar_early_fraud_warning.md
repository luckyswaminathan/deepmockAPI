# Component Plan: `radar.early_fraud_warning`

**API Slug:** `stripe`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /v1/radar/early_fraud_warnings/{early_fraud_warning}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `radar.early_fraud_warning`
  - Filters:
    - `early_fraud_warning` eq `path.early_fraud_warning`
  - Notes:
    - Response body references #/components/schemas/radar.early_fraud_warning
    - Query parameters: expand
