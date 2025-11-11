# Component Plan: `api.v2010.account.call.user_defined_message`

**API Slug:** `twilio`
**Total Routes:** 1

## Supported Operations
- **`create`**: Create a new record for the component.

## Routes

### POST Routes (1)

#### `POST /2010-04-01/Accounts/{AccountSid}/Calls/{CallSid}/UserDefinedMessages.json`
**Summary:** Create a new User Defined Message for the given Call SID.
**Status:** planned

**Operations:**
- **create**
  - Component: `api.v2010.account.call.user_defined_message`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `CallSid` eq `path.CallSid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.call.user_defined_message
    - Query parameters: AccountSid, CallSid
