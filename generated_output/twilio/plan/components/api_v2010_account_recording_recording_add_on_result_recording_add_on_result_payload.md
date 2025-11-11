# Component Plan: `api.v2010.account.recording.recording_add_on_result.recording_add_on_result_payload`

**API Slug:** `twilio`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /2010-04-01/Accounts/{AccountSid}/Recordings/{ReferenceSid}/AddOnResults/{AddOnResultSid}/Payloads/{Sid}.json`
**Summary:** Fetch an instance of a result payload
**Status:** planned

**Operations:**
- **read_one**
  - Component: `api.v2010.account.recording.recording_add_on_result.recording_add_on_result_payload`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `ReferenceSid` eq `path.ReferenceSid`
    - `AddOnResultSid` eq `path.AddOnResultSid`
    - `sid` eq `path.Sid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.recording.recording_add_on_result.recording_add_on_result_payload
    - Query parameters: AccountSid, ReferenceSid, AddOnResultSid, Sid
