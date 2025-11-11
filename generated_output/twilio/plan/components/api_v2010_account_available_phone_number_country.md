# Component Plan: `api.v2010.account.available_phone_number_country`

**API Slug:** `twilio`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /2010-04-01/Accounts/{AccountSid}/AvailablePhoneNumbers/{CountryCode}.json`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `api.v2010.account.available_phone_number_country`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `CountryCode` eq `path.CountryCode`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.available_phone_number_country
    - Query parameters: AccountSid, CountryCode
