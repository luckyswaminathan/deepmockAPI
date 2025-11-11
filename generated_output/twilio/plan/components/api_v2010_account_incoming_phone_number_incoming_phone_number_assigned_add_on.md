# Component Plan: `api.v2010.account.incoming_phone_number.incoming_phone_number_assigned_add_on`

**API Slug:** `twilio`
**Total Routes:** 2

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /2010-04-01/Accounts/{AccountSid}/IncomingPhoneNumbers/{ResourceSid}/AssignedAddOns/{Sid}.json`
**Summary:** Fetch an instance of an Add-on installation currently assigned to this Number.
**Status:** planned

**Operations:**
- **read_one**
  - Component: `api.v2010.account.incoming_phone_number.incoming_phone_number_assigned_add_on`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `ResourceSid` eq `path.ResourceSid`
    - `sid` eq `path.Sid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.incoming_phone_number.incoming_phone_number_assigned_add_on
    - Query parameters: AccountSid, ResourceSid, Sid

### POST Routes (1)

#### `POST /2010-04-01/Accounts/{AccountSid}/IncomingPhoneNumbers/{ResourceSid}/AssignedAddOns.json`
**Summary:** Assign an Add-on installation to the Number specified.
**Status:** planned

**Operations:**
- **create**
  - Component: `api.v2010.account.incoming_phone_number.incoming_phone_number_assigned_add_on`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `ResourceSid` eq `path.ResourceSid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.incoming_phone_number.incoming_phone_number_assigned_add_on
    - Query parameters: AccountSid, ResourceSid
