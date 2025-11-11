# Component Plan: `api.v2010.account.usage.usage_trigger`

**API Slug:** `twilio`
**Total Routes:** 3

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /2010-04-01/Accounts/{AccountSid}/Usage/Triggers/{Sid}.json`
**Summary:** Fetch and instance of a usage-trigger
**Status:** planned

**Operations:**
- **read_one**
  - Component: `api.v2010.account.usage.usage_trigger`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `sid` eq `path.Sid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.usage.usage_trigger
    - Query parameters: AccountSid, Sid

### POST Routes (2)

#### `POST /2010-04-01/Accounts/{AccountSid}/Usage/Triggers.json`
**Summary:** Create a new UsageTrigger
**Status:** planned

**Operations:**
- **create**
  - Component: `api.v2010.account.usage.usage_trigger`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.usage.usage_trigger
    - Query parameters: AccountSid

#### `POST /2010-04-01/Accounts/{AccountSid}/Usage/Triggers/{Sid}.json`
**Summary:** Update an instance of a usage trigger
**Status:** planned

**Operations:**
- **create**
  - Component: `api.v2010.account.usage.usage_trigger`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `sid` eq `path.Sid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.usage.usage_trigger
    - Query parameters: AccountSid, Sid
