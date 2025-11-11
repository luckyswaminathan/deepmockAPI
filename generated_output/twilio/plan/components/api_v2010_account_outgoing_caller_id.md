# Component Plan: `api.v2010.account.outgoing_caller_id`

**API Slug:** `twilio`
**Total Routes:** 2

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /2010-04-01/Accounts/{AccountSid}/OutgoingCallerIds/{Sid}.json`
**Summary:** Fetch an outgoing-caller-id belonging to the account used to make the request
**Status:** planned

**Operations:**
- **read_one**
  - Component: `api.v2010.account.outgoing_caller_id`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `sid` eq `path.Sid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.outgoing_caller_id
    - Query parameters: AccountSid, Sid

### POST Routes (1)

#### `POST /2010-04-01/Accounts/{AccountSid}/OutgoingCallerIds/{Sid}.json`
**Summary:** Updates the caller-id
**Status:** planned

**Operations:**
- **create**
  - Component: `api.v2010.account.outgoing_caller_id`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `sid` eq `path.Sid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.outgoing_caller_id
    - Query parameters: AccountSid, Sid
