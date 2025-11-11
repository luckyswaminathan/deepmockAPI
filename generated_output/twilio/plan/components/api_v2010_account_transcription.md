# Component Plan: `api.v2010.account.transcription`

**API Slug:** `twilio`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /2010-04-01/Accounts/{AccountSid}/Transcriptions/{Sid}.json`
**Summary:** Fetch an instance of a Transcription
**Status:** planned

**Operations:**
- **read_one**
  - Component: `api.v2010.account.transcription`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `sid` eq `path.Sid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.transcription
    - Query parameters: AccountSid, Sid
