# Component Plan: `api.v2010.account.call.stream`

**API Slug:** `twilio`
**Total Routes:** 2

## Supported Operations
- **`create`**: Create a new record for the component.

## Routes

### POST Routes (2)

#### `POST /2010-04-01/Accounts/{AccountSid}/Calls/{CallSid}/Streams.json`
**Summary:** Create a Stream
**Status:** planned

**Operations:**
- **create**
  - Component: `api.v2010.account.call.stream`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `CallSid` eq `path.CallSid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.call.stream
    - Query parameters: AccountSid, CallSid

#### `POST /2010-04-01/Accounts/{AccountSid}/Calls/{CallSid}/Streams/{Sid}.json`
**Summary:** Stop a Stream using either the SID of the Stream resource or the `name` used when creating the resource
**Status:** planned

**Operations:**
- **create**
  - Component: `api.v2010.account.call.stream`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `CallSid` eq `path.CallSid`
    - `sid` eq `path.Sid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.call.stream
    - Query parameters: AccountSid, CallSid, Sid
