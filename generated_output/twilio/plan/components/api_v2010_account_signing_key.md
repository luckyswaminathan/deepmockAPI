# Component Plan: `api.v2010.account.signing_key`

**API Slug:** `twilio`
**Total Routes:** 2

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /2010-04-01/Accounts/{AccountSid}/SigningKeys/{Sid}.json`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `api.v2010.account.signing_key`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `sid` eq `path.Sid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.signing_key
    - Query parameters: AccountSid, Sid

### POST Routes (1)

#### `POST /2010-04-01/Accounts/{AccountSid}/SigningKeys/{Sid}.json`
**Status:** planned

**Operations:**
- **create**
  - Component: `api.v2010.account.signing_key`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `sid` eq `path.Sid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.signing_key
    - Query parameters: AccountSid, Sid
