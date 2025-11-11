# Component Plan: `api.v2010.account.sip.sip_domain`

**API Slug:** `twilio`
**Total Routes:** 3

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /2010-04-01/Accounts/{AccountSid}/SIP/Domains/{Sid}.json`
**Summary:** Fetch an instance of a Domain
**Status:** planned

**Operations:**
- **read_one**
  - Component: `api.v2010.account.sip.sip_domain`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `sid` eq `path.Sid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.sip.sip_domain
    - Query parameters: AccountSid, Sid

### POST Routes (2)

#### `POST /2010-04-01/Accounts/{AccountSid}/SIP/Domains.json`
**Summary:** Create a new Domain
**Status:** planned

**Operations:**
- **create**
  - Component: `api.v2010.account.sip.sip_domain`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.sip.sip_domain
    - Query parameters: AccountSid

#### `POST /2010-04-01/Accounts/{AccountSid}/SIP/Domains/{Sid}.json`
**Summary:** Update the attributes of a domain
**Status:** planned

**Operations:**
- **create**
  - Component: `api.v2010.account.sip.sip_domain`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `sid` eq `path.Sid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.sip.sip_domain
    - Query parameters: AccountSid, Sid
