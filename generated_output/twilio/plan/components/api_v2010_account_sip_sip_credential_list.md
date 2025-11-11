# Component Plan: `api.v2010.account.sip.sip_credential_list`

**API Slug:** `twilio`
**Total Routes:** 3

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /2010-04-01/Accounts/{AccountSid}/SIP/CredentialLists/{Sid}.json`
**Summary:** Get a Credential List
**Status:** planned

**Operations:**
- **read_one**
  - Component: `api.v2010.account.sip.sip_credential_list`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `sid` eq `path.Sid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.sip.sip_credential_list
    - Query parameters: AccountSid, Sid

### POST Routes (2)

#### `POST /2010-04-01/Accounts/{AccountSid}/SIP/CredentialLists.json`
**Summary:** Create a Credential List
**Status:** planned

**Operations:**
- **create**
  - Component: `api.v2010.account.sip.sip_credential_list`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.sip.sip_credential_list
    - Query parameters: AccountSid

#### `POST /2010-04-01/Accounts/{AccountSid}/SIP/CredentialLists/{Sid}.json`
**Summary:** Update a Credential List
**Status:** planned

**Operations:**
- **create**
  - Component: `api.v2010.account.sip.sip_credential_list`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `sid` eq `path.Sid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.sip.sip_credential_list
    - Query parameters: AccountSid, Sid
