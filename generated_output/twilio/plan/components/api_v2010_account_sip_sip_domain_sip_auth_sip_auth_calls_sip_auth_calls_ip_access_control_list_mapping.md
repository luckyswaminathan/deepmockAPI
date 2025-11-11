# Component Plan: `api.v2010.account.sip.sip_domain.sip_auth.sip_auth_calls.sip_auth_calls_ip_access_control_list_mapping`

**API Slug:** `twilio`
**Total Routes:** 2

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /2010-04-01/Accounts/{AccountSid}/SIP/Domains/{DomainSid}/Auth/Calls/IpAccessControlListMappings/{Sid}.json`
**Summary:** Fetch a specific instance of an IP Access Control List mapping
**Status:** planned

**Operations:**
- **read_one**
  - Component: `api.v2010.account.sip.sip_domain.sip_auth.sip_auth_calls.sip_auth_calls_ip_access_control_list_mapping`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `DomainSid` eq `path.DomainSid`
    - `sid` eq `path.Sid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.sip.sip_domain.sip_auth.sip_auth_calls.sip_auth_calls_ip_access_control_list_mapping
    - Query parameters: AccountSid, DomainSid, Sid

### POST Routes (1)

#### `POST /2010-04-01/Accounts/{AccountSid}/SIP/Domains/{DomainSid}/Auth/Calls/IpAccessControlListMappings.json`
**Summary:** Create a new IP Access Control List mapping
**Status:** planned

**Operations:**
- **create**
  - Component: `api.v2010.account.sip.sip_domain.sip_auth.sip_auth_calls.sip_auth_calls_ip_access_control_list_mapping`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `DomainSid` eq `path.DomainSid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.sip.sip_domain.sip_auth.sip_auth_calls.sip_auth_calls_ip_access_control_list_mapping
    - Query parameters: AccountSid, DomainSid
