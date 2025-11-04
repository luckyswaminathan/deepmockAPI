# Component Plan: `person`

**API Slug:** `stripe`
**Total Routes:** 8

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (1)

#### `DELETE /v1/accounts/{account}/persons/{person}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `person`
  - Filters:
    - `account` eq `path.account`
    - `person` eq `path.person`
  - Notes:
    - Query parameters: account, person

### GET Routes (3)

#### `GET /v1/accounts/{account}/people/{person}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `person`
  - Filters:
    - `account` eq `path.account`
    - `person` eq `path.person`
  - Notes:
    - Response body references #/components/schemas/person
    - Query parameters: expand

#### `GET /v1/accounts/{account}/persons`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `person`
  - Filters:
    - `account` eq `path.account`
  - Notes:
    - Query parameters: ending_before, expand, limit, relationship, starting_after

#### `GET /v1/accounts/{account}/persons/{person}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `person`
  - Filters:
    - `account` eq `path.account`
    - `person` eq `path.person`
  - Notes:
    - Response body references #/components/schemas/person
    - Query parameters: expand

### POST Routes (4)

#### `POST /v1/accounts/{account}/people`
**Status:** planned

**Operations:**
- **create**
  - Component: `person`
  - Filters:
    - `account` eq `path.account`
  - Notes:
    - Response body references #/components/schemas/person
    - Query parameters: account

#### `POST /v1/accounts/{account}/people/{person}`
**Status:** planned

**Operations:**
- **create**
  - Component: `person`
  - Filters:
    - `account` eq `path.account`
    - `person` eq `path.person`
  - Notes:
    - Response body references #/components/schemas/person
    - Query parameters: account, person

#### `POST /v1/accounts/{account}/persons`
**Status:** planned

**Operations:**
- **create**
  - Component: `person`
  - Filters:
    - `account` eq `path.account`
  - Notes:
    - Response body references #/components/schemas/person
    - Query parameters: account

#### `POST /v1/accounts/{account}/persons/{person}`
**Status:** planned

**Operations:**
- **create**
  - Component: `person`
  - Filters:
    - `account` eq `path.account`
    - `person` eq `path.person`
  - Notes:
    - Response body references #/components/schemas/person
    - Query parameters: account, person
