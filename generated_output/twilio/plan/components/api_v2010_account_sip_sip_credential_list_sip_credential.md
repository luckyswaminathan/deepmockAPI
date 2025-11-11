# Component Plan: `api.v2010.account.sip.sip_credential_list.sip_credential`

**API Slug:** `twilio`
**Total Routes:** 3

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /2010-04-01/Accounts/{AccountSid}/SIP/CredentialLists/{CredentialListSid}/Credentials/{Sid}.json`
**Summary:** Fetch a single credential.
**Status:** planned

**Operations:**
- **read_one**
  - Component: `api.v2010.account.sip.sip_credential_list.sip_credential`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `CredentialListSid` eq `path.CredentialListSid`
    - `sid` eq `path.Sid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.sip.sip_credential_list.sip_credential
    - Query parameters: AccountSid, CredentialListSid, Sid

### POST Routes (2)

#### `POST /2010-04-01/Accounts/{AccountSid}/SIP/CredentialLists/{CredentialListSid}/Credentials.json`
**Summary:** Create a new credential resource.
**Status:** planned

**Operations:**
- **create**
  - Component: `api.v2010.account.sip.sip_credential_list.sip_credential`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `CredentialListSid` eq `path.CredentialListSid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.sip.sip_credential_list.sip_credential
    - Query parameters: AccountSid, CredentialListSid

#### `POST /2010-04-01/Accounts/{AccountSid}/SIP/CredentialLists/{CredentialListSid}/Credentials/{Sid}.json`
**Summary:** Update a credential resource.
**Status:** planned

**Operations:**
- **create**
  - Component: `api.v2010.account.sip.sip_credential_list.sip_credential`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `CredentialListSid` eq `path.CredentialListSid`
    - `sid` eq `path.Sid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.sip.sip_credential_list.sip_credential
    - Query parameters: AccountSid, CredentialListSid, Sid
