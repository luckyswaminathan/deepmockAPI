# Component Plan: `api.v2010.account.call.user_defined_message_subscription`

**API Slug:** `twilio`
**Total Routes:** 1

## Supported Operations
- **`create`**: Create a new record for the component.

## Routes

### POST Routes (1)

#### `POST /2010-04-01/Accounts/{AccountSid}/Calls/{CallSid}/UserDefinedMessageSubscriptions.json`
**Summary:** Subscribe to User Defined Messages for a given Call SID.
**Status:** planned

**Operations:**
- **create**
  - Component: `api.v2010.account.call.user_defined_message_subscription`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `CallSid` eq `path.CallSid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.call.user_defined_message_subscription
    - Query parameters: AccountSid, CallSid
