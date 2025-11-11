# Component Plan: `api.v2010.account.call.payments`

**API Slug:** `twilio`
**Total Routes:** 2

## Supported Operations
- **`create`**: Create a new record for the component.

## Routes

### POST Routes (2)

#### `POST /2010-04-01/Accounts/{AccountSid}/Calls/{CallSid}/Payments.json`
**Summary:** create an instance of payments. This will start a new payments session
**Status:** planned

**Operations:**
- **create**
  - Component: `api.v2010.account.call.payments`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `CallSid` eq `path.CallSid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.call.payments
    - Query parameters: AccountSid, CallSid

#### `POST /2010-04-01/Accounts/{AccountSid}/Calls/{CallSid}/Payments/{Sid}.json`
**Summary:** update an instance of payments with different phases of payment flows.
**Status:** planned

**Operations:**
- **create**
  - Component: `api.v2010.account.call.payments`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `CallSid` eq `path.CallSid`
    - `sid` eq `path.Sid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.call.payments
    - Query parameters: AccountSid, CallSid, Sid
