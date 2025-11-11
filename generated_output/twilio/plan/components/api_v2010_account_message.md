# Component Plan: `api.v2010.account.message`

**API Slug:** `twilio`
**Total Routes:** 3

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /2010-04-01/Accounts/{AccountSid}/Messages/{Sid}.json`
**Summary:** Fetch a specific Message
**Status:** planned

**Operations:**
- **read_one**
  - Component: `api.v2010.account.message`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `sid` eq `path.Sid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.message
    - Query parameters: AccountSid, Sid

### POST Routes (2)

#### `POST /2010-04-01/Accounts/{AccountSid}/Messages.json`
**Summary:** Send a message
**Status:** planned

**Operations:**
- **create**
  - Component: `api.v2010.account.message`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.message
    - Query parameters: AccountSid

#### `POST /2010-04-01/Accounts/{AccountSid}/Messages/{Sid}.json`
**Summary:** Update a Message resource (used to redact Message `body` text and to cancel not-yet-sent messages)
**Status:** planned

**Operations:**
- **create**
  - Component: `api.v2010.account.message`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `sid` eq `path.Sid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.message
    - Query parameters: AccountSid, Sid
