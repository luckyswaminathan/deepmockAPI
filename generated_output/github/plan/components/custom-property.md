# Component Plan: `custom-property`

**API Slug:** `github`
**Total Routes:** 2

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.
- **`update`**: Replace a full record.

## Routes

### GET Routes (1)

#### `GET /orgs/{org}/properties/schema/{custom_property_name}`
**Summary:** Get a custom property for an organization
**Status:** planned

**Operations:**
- **read_one**
  - Component: `custom-property`
  - Filters:
    - `org` eq `path.org`
    - `custom_property_name` eq `path.custom_property_name`
  - Notes:
    - Response body references #/components/schemas/custom-property

### PUT Routes (1)

#### `PUT /orgs/{org}/properties/schema/{custom_property_name}`
**Summary:** Create or update a custom property for an organization
**Status:** planned

**Operations:**
- **update**
  - Component: `custom-property`
  - Filters:
    - `org` eq `path.org`
    - `custom_property_name` eq `path.custom_property_name`
  - Notes:
    - Response body references #/components/schemas/custom-property
