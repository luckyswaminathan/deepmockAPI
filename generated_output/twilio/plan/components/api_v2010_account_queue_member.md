# Component Plan: `api.v2010.account.queue.member`

**API Slug:** `twilio`
**Total Routes:** 2

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /2010-04-01/Accounts/{AccountSid}/Queues/{QueueSid}/Members/{CallSid}.json`
**Summary:** Fetch a specific member from the queue
**Status:** planned

**Operations:**
- **read_one**
  - Component: `api.v2010.account.queue.member`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `QueueSid` eq `path.QueueSid`
    - `CallSid` eq `path.CallSid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.queue.member
    - Query parameters: AccountSid, QueueSid, CallSid

### POST Routes (1)

#### `POST /2010-04-01/Accounts/{AccountSid}/Queues/{QueueSid}/Members/{CallSid}.json`
**Summary:** Dequeue a member from a queue and have the member's call begin executing the TwiML document at that URL
**Status:** planned

**Operations:**
- **create**
  - Component: `api.v2010.account.queue.member`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `QueueSid` eq `path.QueueSid`
    - `CallSid` eq `path.CallSid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.queue.member
    - Query parameters: AccountSid, QueueSid, CallSid
