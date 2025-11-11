# Component Plan: `api.v2010.account.call.siprec`

**API Slug:** `twilio`
**Total Routes:** 2

## Supported Operations
- **`create`**: Create a new record for the component.

## Routes

### POST Routes (2)

#### `POST /2010-04-01/Accounts/{AccountSid}/Calls/{CallSid}/Siprec.json`
**Summary:** Create a Siprec
**Status:** planned

**Operations:**
- **create**
  - Component: `api.v2010.account.call.siprec`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `CallSid` eq `path.CallSid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.call.siprec
    - Query parameters: AccountSid, CallSid

#### `POST /2010-04-01/Accounts/{AccountSid}/Calls/{CallSid}/Siprec/{Sid}.json`
**Summary:** Stop a Siprec using either the SID of the Siprec resource or the `name` used when creating the resource
**Status:** planned

**Operations:**
- **create**
  - Component: `api.v2010.account.call.siprec`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `CallSid` eq `path.CallSid`
    - `sid` eq `path.Sid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.call.siprec
    - Query parameters: AccountSid, CallSid, Sid
