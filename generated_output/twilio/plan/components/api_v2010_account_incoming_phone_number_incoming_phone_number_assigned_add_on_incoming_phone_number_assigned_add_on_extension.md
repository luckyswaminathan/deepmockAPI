# Component Plan: `api.v2010.account.incoming_phone_number.incoming_phone_number_assigned_add_on.incoming_phone_number_assigned_add_on_extension`

**API Slug:** `twilio`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /2010-04-01/Accounts/{AccountSid}/IncomingPhoneNumbers/{ResourceSid}/AssignedAddOns/{AssignedAddOnSid}/Extensions/{Sid}.json`
**Summary:** Fetch an instance of an Extension for the Assigned Add-on.
**Status:** planned

**Operations:**
- **read_one**
  - Component: `api.v2010.account.incoming_phone_number.incoming_phone_number_assigned_add_on.incoming_phone_number_assigned_add_on_extension`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `ResourceSid` eq `path.ResourceSid`
    - `AssignedAddOnSid` eq `path.AssignedAddOnSid`
    - `sid` eq `path.Sid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.incoming_phone_number.incoming_phone_number_assigned_add_on.incoming_phone_number_assigned_add_on_extension
    - Query parameters: AccountSid, ResourceSid, AssignedAddOnSid, Sid
