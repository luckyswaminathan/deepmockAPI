# Component Plan: `api.v2010.account.incoming_phone_number.incoming_phone_number_mobile`

**API Slug:** `twilio`
**Total Routes:** 1

## Supported Operations
- **`create`**: Create a new record for the component.

## Routes

### POST Routes (1)

#### `POST /2010-04-01/Accounts/{AccountSid}/IncomingPhoneNumbers/Mobile.json`
**Status:** planned

**Operations:**
- **create**
  - Component: `api.v2010.account.incoming_phone_number.incoming_phone_number_mobile`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.incoming_phone_number.incoming_phone_number_mobile
    - Query parameters: AccountSid
