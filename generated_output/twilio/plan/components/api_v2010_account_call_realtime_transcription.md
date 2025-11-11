# Component Plan: `api.v2010.account.call.realtime_transcription`

**API Slug:** `twilio`
**Total Routes:** 2

## Supported Operations
- **`create`**: Create a new record for the component.

## Routes

### POST Routes (2)

#### `POST /2010-04-01/Accounts/{AccountSid}/Calls/{CallSid}/Transcriptions.json`
**Summary:** Create a Transcription
**Status:** planned

**Operations:**
- **create**
  - Component: `api.v2010.account.call.realtime_transcription`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `CallSid` eq `path.CallSid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.call.realtime_transcription
    - Query parameters: AccountSid, CallSid

#### `POST /2010-04-01/Accounts/{AccountSid}/Calls/{CallSid}/Transcriptions/{Sid}.json`
**Summary:** Stop a Transcription using either the SID of the Transcription resource or the `name` used when creating the resource
**Status:** planned

**Operations:**
- **create**
  - Component: `api.v2010.account.call.realtime_transcription`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `CallSid` eq `path.CallSid`
    - `sid` eq `path.Sid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.call.realtime_transcription
    - Query parameters: AccountSid, CallSid, Sid
