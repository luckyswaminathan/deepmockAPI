# Component Plan: `api.v2010.account.token`

**API Slug:** `twilio`
**Total Routes:** 1

## Supported Operations
- **`create`**: Create a new record for the component.

## Routes

### POST Routes (1)

#### `POST /2010-04-01/Accounts/{AccountSid}/Tokens.json`
**Summary:** Create a new token for ICE servers
**Status:** planned

**Operations:**
- **create**
  - Component: `api.v2010.account.token`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.token
    - Query parameters: AccountSid
