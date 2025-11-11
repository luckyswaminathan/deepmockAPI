# Component Plan: `api.v2010.account.incoming_phone_number`

**API Slug:** `twilio`
**Total Routes:** 3

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /2010-04-01/Accounts/{AccountSid}/IncomingPhoneNumbers/{Sid}.json`
**Summary:** Fetch an incoming-phone-number belonging to the account used to make the request.
**Status:** planned

**Operations:**
- **read_one**
  - Component: `api.v2010.account.incoming_phone_number`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `sid` eq `path.Sid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.incoming_phone_number
    - Query parameters: AccountSid, Sid

### POST Routes (2)

#### `POST /2010-04-01/Accounts/{AccountSid}/IncomingPhoneNumbers.json`
**Summary:** Purchase a phone-number for the account.
**Status:** planned

**Operations:**
- **create**
  - Component: `api.v2010.account.incoming_phone_number`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.incoming_phone_number
    - Query parameters: AccountSid

#### `POST /2010-04-01/Accounts/{AccountSid}/IncomingPhoneNumbers/{Sid}.json`
**Summary:** Update an incoming-phone-number instance.
**Status:** planned

**Operations:**
- **create**
  - Component: `api.v2010.account.incoming_phone_number`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `sid` eq `path.Sid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.incoming_phone_number
    - Query parameters: AccountSid, Sid
