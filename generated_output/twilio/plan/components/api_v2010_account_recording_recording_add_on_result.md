# Component Plan: `api.v2010.account.recording.recording_add_on_result`

**API Slug:** `twilio`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /2010-04-01/Accounts/{AccountSid}/Recordings/{ReferenceSid}/AddOnResults/{Sid}.json`
**Summary:** Fetch an instance of an AddOnResult
**Status:** planned

**Operations:**
- **read_one**
  - Component: `api.v2010.account.recording.recording_add_on_result`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `ReferenceSid` eq `path.ReferenceSid`
    - `sid` eq `path.Sid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.recording.recording_add_on_result
    - Query parameters: AccountSid, ReferenceSid, Sid
