# Component Plan: `api.v2010.account.application`

**API Slug:** `twilio`
**Total Routes:** 3

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /2010-04-01/Accounts/{AccountSid}/Applications/{Sid}.json`
**Summary:** Fetch the application specified by the provided sid
**Status:** planned

**Operations:**
- **read_one**
  - Component: `api.v2010.account.application`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `sid` eq `path.Sid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.application
    - Query parameters: AccountSid, Sid

### POST Routes (2)

#### `POST /2010-04-01/Accounts/{AccountSid}/Applications.json`
**Summary:** Create a new application within your account
**Status:** planned

**Operations:**
- **create**
  - Component: `api.v2010.account.application`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.application
    - Query parameters: AccountSid

#### `POST /2010-04-01/Accounts/{AccountSid}/Applications/{Sid}.json`
**Summary:** Updates the application's properties
**Status:** planned

**Operations:**
- **create**
  - Component: `api.v2010.account.application`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `sid` eq `path.Sid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.application
    - Query parameters: AccountSid, Sid
