# Component Plan: `api.v2010.account.conference.conference_recording`

**API Slug:** `twilio`
**Total Routes:** 2

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /2010-04-01/Accounts/{AccountSid}/Conferences/{ConferenceSid}/Recordings/{Sid}.json`
**Summary:** Fetch an instance of a recording for a call
**Status:** planned

**Operations:**
- **read_one**
  - Component: `api.v2010.account.conference.conference_recording`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `ConferenceSid` eq `path.ConferenceSid`
    - `sid` eq `path.Sid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.conference.conference_recording
    - Query parameters: AccountSid, ConferenceSid, Sid

### POST Routes (1)

#### `POST /2010-04-01/Accounts/{AccountSid}/Conferences/{ConferenceSid}/Recordings/{Sid}.json`
**Summary:** Changes the status of the recording to paused, stopped, or in-progress. Note: To use `Twilio.CURRENT`, pass it as recording sid.
**Status:** planned

**Operations:**
- **create**
  - Component: `api.v2010.account.conference.conference_recording`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `ConferenceSid` eq `path.ConferenceSid`
    - `sid` eq `path.Sid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.conference.conference_recording
    - Query parameters: AccountSid, ConferenceSid, Sid
