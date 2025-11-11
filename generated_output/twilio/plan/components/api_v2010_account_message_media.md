# Component Plan: `api.v2010.account.message.media`

**API Slug:** `twilio`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /2010-04-01/Accounts/{AccountSid}/Messages/{MessageSid}/Media/{Sid}.json`
**Summary:** Fetch a single Media resource associated with a specific Message resource
**Status:** planned

**Operations:**
- **read_one**
  - Component: `api.v2010.account.message.media`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `MessageSid` eq `path.MessageSid`
    - `sid` eq `path.Sid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.message.media
    - Query parameters: AccountSid, MessageSid, Sid
