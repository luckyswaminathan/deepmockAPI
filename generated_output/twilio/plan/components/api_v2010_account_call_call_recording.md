# Component Plan: `api.v2010.account.call.call_recording`

**API Slug:** `twilio`
**Total Routes:** 3

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /2010-04-01/Accounts/{AccountSid}/Calls/{CallSid}/Recordings/{Sid}.json`
**Summary:** Fetch an instance of a recording for a call
**Status:** planned

**Operations:**
- **read_one**
  - Component: `api.v2010.account.call.call_recording`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `CallSid` eq `path.CallSid`
    - `sid` eq `path.Sid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.call.call_recording
    - Query parameters: AccountSid, CallSid, Sid

### POST Routes (2)

#### `POST /2010-04-01/Accounts/{AccountSid}/Calls/{CallSid}/Recordings.json`
**Summary:** Create a recording for the call
**Status:** planned

**Operations:**
- **create**
  - Component: `api.v2010.account.call.call_recording`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `CallSid` eq `path.CallSid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.call.call_recording
    - Query parameters: AccountSid, CallSid

#### `POST /2010-04-01/Accounts/{AccountSid}/Calls/{CallSid}/Recordings/{Sid}.json`
**Summary:** Changes the status of the recording to paused, stopped, or in-progress. Note: Pass `Twilio.CURRENT` instead of recording sid to reference current active recording.
**Status:** planned

**Operations:**
- **create**
  - Component: `api.v2010.account.call.call_recording`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `CallSid` eq `path.CallSid`
    - `sid` eq `path.Sid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.call.call_recording
    - Query parameters: AccountSid, CallSid, Sid
