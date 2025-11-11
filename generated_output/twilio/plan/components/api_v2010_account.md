# Component Plan: `api.v2010.account`

**API Slug:** `twilio`
**Total Routes:** 3

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /2010-04-01/Accounts/{Sid}.json`
**Summary:** Fetch the account specified by the provided Account Sid
**Status:** planned

**Operations:**
- **read_one**
  - Component: `api.v2010.account`
  - Filters:
    - `sid` eq `path.Sid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account
    - Query parameters: Sid

### POST Routes (2)

#### `POST /2010-04-01/Accounts.json`
**Summary:** Create a new Twilio Subaccount from the account making the request
**Status:** planned

**Operations:**
- **create**
  - Component: `api.v2010.account`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account

#### `POST /2010-04-01/Accounts/{Sid}.json`
**Summary:** Modify the properties of a given Account
**Status:** planned

**Operations:**
- **create**
  - Component: `api.v2010.account`
  - Filters:
    - `sid` eq `path.Sid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account
    - Query parameters: Sid
