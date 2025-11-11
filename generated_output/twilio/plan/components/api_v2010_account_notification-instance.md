# Component Plan: `api.v2010.account.notification-instance`

**API Slug:** `twilio`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /2010-04-01/Accounts/{AccountSid}/Notifications/{Sid}.json`
**Summary:** Fetch a notification belonging to the account used to make the request
**Status:** planned

**Operations:**
- **read_one**
  - Component: `api.v2010.account.notification-instance`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `sid` eq `path.Sid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.notification-instance
    - Query parameters: AccountSid, Sid
