# Component Plan: `api.v2010.account.call`

**API Slug:** `twilio`
**Total Routes:** 3

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /2010-04-01/Accounts/{AccountSid}/Calls/{Sid}.json`
**Summary:** Fetch the call specified by the provided Call SID
**Status:** planned

**Operations:**
- **read_one**
  - Component: `api.v2010.account.call`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `sid` eq `path.Sid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.call
    - Query parameters: AccountSid, Sid

### POST Routes (2)

#### `POST /2010-04-01/Accounts/{AccountSid}/Calls.json`
**Summary:** Create a new outgoing call to phones, SIP-enabled endpoints or Twilio Client connections
**Status:** planned

**Operations:**
- **create**
  - Component: `api.v2010.account.call`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.call
    - Query parameters: AccountSid

#### `POST /2010-04-01/Accounts/{AccountSid}/Calls/{Sid}.json`
**Summary:** Initiates a call redirect or terminates a call
**Status:** planned

**Operations:**
- **create**
  - Component: `api.v2010.account.call`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `sid` eq `path.Sid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.call
    - Query parameters: AccountSid, Sid
