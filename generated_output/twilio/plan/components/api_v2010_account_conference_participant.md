# Component Plan: `api.v2010.account.conference.participant`

**API Slug:** `twilio`
**Total Routes:** 3

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /2010-04-01/Accounts/{AccountSid}/Conferences/{ConferenceSid}/Participants/{CallSid}.json`
**Summary:** Fetch an instance of a participant
**Status:** planned

**Operations:**
- **read_one**
  - Component: `api.v2010.account.conference.participant`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `ConferenceSid` eq `path.ConferenceSid`
    - `CallSid` eq `path.CallSid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.conference.participant
    - Query parameters: AccountSid, ConferenceSid, CallSid

### POST Routes (2)

#### `POST /2010-04-01/Accounts/{AccountSid}/Conferences/{ConferenceSid}/Participants.json`
**Status:** planned

**Operations:**
- **create**
  - Component: `api.v2010.account.conference.participant`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `ConferenceSid` eq `path.ConferenceSid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.conference.participant
    - Query parameters: AccountSid, ConferenceSid

#### `POST /2010-04-01/Accounts/{AccountSid}/Conferences/{ConferenceSid}/Participants/{CallSid}.json`
**Summary:** Update the properties of the participant
**Status:** planned

**Operations:**
- **create**
  - Component: `api.v2010.account.conference.participant`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `ConferenceSid` eq `path.ConferenceSid`
    - `CallSid` eq `path.CallSid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.conference.participant
    - Query parameters: AccountSid, ConferenceSid, CallSid
