# Component Plan: `api.v2010.account.incoming_phone_number.incoming_phone_number_toll_free`

**API Slug:** `twilio`
**Total Routes:** 1

## Supported Operations
- **`create`**: Create a new record for the component.

## Routes

### POST Routes (1)

#### `POST /2010-04-01/Accounts/{AccountSid}/IncomingPhoneNumbers/TollFree.json`
**Status:** planned

**Operations:**
- **create**
  - Component: `api.v2010.account.incoming_phone_number.incoming_phone_number_toll_free`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.incoming_phone_number.incoming_phone_number_toll_free
    - Query parameters: AccountSid
