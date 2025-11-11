# Component Plan: `api.v2010.account.recording.recording_transcription`

**API Slug:** `twilio`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /2010-04-01/Accounts/{AccountSid}/Recordings/{RecordingSid}/Transcriptions/{Sid}.json`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `api.v2010.account.recording.recording_transcription`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `RecordingSid` eq `path.RecordingSid`
    - `sid` eq `path.Sid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.recording.recording_transcription
    - Query parameters: AccountSid, RecordingSid, Sid
