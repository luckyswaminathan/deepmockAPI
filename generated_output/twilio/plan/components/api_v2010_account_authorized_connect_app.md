# Component Plan: `api.v2010.account.authorized_connect_app`

**API Slug:** `twilio`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /2010-04-01/Accounts/{AccountSid}/AuthorizedConnectApps/{ConnectAppSid}.json`
**Summary:** Fetch an instance of an authorized-connect-app
**Status:** planned

**Operations:**
- **read_one**
  - Component: `api.v2010.account.authorized_connect_app`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `ConnectAppSid` eq `path.ConnectAppSid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.authorized_connect_app
    - Query parameters: AccountSid, ConnectAppSid
