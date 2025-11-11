# Component Plan: `api.v2010.account.new_signing_key`

**API Slug:** `twilio`
**Total Routes:** 1

## Supported Operations
- **`create`**: Create a new record for the component.

## Routes

### POST Routes (1)

#### `POST /2010-04-01/Accounts/{AccountSid}/SigningKeys.json`
**Summary:** Create a new Signing Key for the account making the request.
**Status:** planned

**Operations:**
- **create**
  - Component: `api.v2010.account.new_signing_key`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.new_signing_key
    - Query parameters: AccountSid
