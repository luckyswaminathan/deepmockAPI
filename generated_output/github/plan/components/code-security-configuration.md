# Component Plan: `code-security-configuration`

**API Slug:** `github`
**Total Routes:** 3

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`update_partial`**: Apply a partial update to a record.

## Routes

### GET Routes (1)

#### `GET /orgs/{org}/code-security/configurations/{configuration_id}`
**Summary:** Get a code security configuration
**Status:** planned

**Operations:**
- **read_one**
  - Component: `code-security-configuration`
  - Filters:
    - `org` eq `path.org`
    - `configuration_id` eq `path.configuration_id`
  - Notes:
    - Response body references #/components/schemas/code-security-configuration

### PATCH Routes (1)

#### `PATCH /orgs/{org}/code-security/configurations/{configuration_id}`
**Summary:** Update a code security configuration
**Status:** planned

**Operations:**
- **update_partial**
  - Component: `code-security-configuration`
  - Filters:
    - `org` eq `path.org`
    - `configuration_id` eq `path.configuration_id`
  - Notes:
    - Response body references #/components/schemas/code-security-configuration

### POST Routes (1)

#### `POST /orgs/{org}/code-security/configurations`
**Summary:** Create a code security configuration
**Status:** planned

**Operations:**
- **create**
  - Component: `code-security-configuration`
  - Filters:
    - `org` eq `path.org`
  - Notes:
    - Response body references #/components/schemas/code-security-configuration
