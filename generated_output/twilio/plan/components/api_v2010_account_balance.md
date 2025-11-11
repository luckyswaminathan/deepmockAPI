# Component Plan: `api.v2010.account.balance`

**API Slug:** `twilio`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /2010-04-01/Accounts/{AccountSid}/Balance.json`
**Summary:** Fetch the balance for an Account based on Account Sid. Balance changes may not be reflected immediately. Child accounts do not contain balance information
**Status:** planned

**Operations:**
- **read_one**
  - Component: `api.v2010.account.balance`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.balance
    - Query parameters: AccountSid
