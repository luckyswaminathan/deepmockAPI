# Component Plan: `api.v2010.account.call.call_notification-instance`

**API Slug:** `twilio`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /2010-04-01/Accounts/{AccountSid}/Calls/{CallSid}/Notifications/{Sid}.json`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `api.v2010.account.call.call_notification-instance`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `CallSid` eq `path.CallSid`
    - `sid` eq `path.Sid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.call.call_notification-instance
    - Query parameters: AccountSid, CallSid, Sid
