# Component Plan: `package`

**API Slug:** `github`
**Total Routes:** 9

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (3)

#### `DELETE /orgs/{org}/packages/{package_type}/{package_name}`
**Summary:** Delete a package for an organization
**Status:** planned

**Operations:**
- **delete**
  - Component: `package`
  - Filters:
    - `org` eq `path.org`
    - `package_type` eq `path.package_type`
    - `package_name` eq `path.package_name`

#### `DELETE /user/packages/{package_type}/{package_name}`
**Summary:** Delete a package for the authenticated user
**Status:** planned

**Operations:**
- **delete**
  - Component: `package`
  - Filters:
    - `package_type` eq `path.package_type`
    - `package_name` eq `path.package_name`

#### `DELETE /users/{username}/packages/{package_type}/{package_name}`
**Summary:** Delete a package for a user
**Status:** planned

**Operations:**
- **delete**
  - Component: `package`
  - Filters:
    - `username` eq `path.username`
    - `package_type` eq `path.package_type`
    - `package_name` eq `path.package_name`

### GET Routes (6)

#### `GET /orgs/{org}/packages`
**Summary:** List packages for an organization
**Status:** planned

**Operations:**
- **read_one**
  - Component: `package`
  - Filters:
    - `org` eq `path.org`
  - Notes:
    - Query parameters: package_type, page, per_page

#### `GET /orgs/{org}/packages/{package_type}/{package_name}`
**Summary:** Get a package for an organization
**Status:** planned

**Operations:**
- **read_one**
  - Component: `package`
  - Filters:
    - `org` eq `path.org`
    - `package_type` eq `path.package_type`
    - `package_name` eq `path.package_name`
  - Notes:
    - Response body references #/components/schemas/package

#### `GET /user/packages`
**Summary:** List packages for the authenticated user's namespace
**Status:** planned

**Operations:**
- **read_many**
  - Component: `package`
  - Notes:
    - Query parameters: package_type

#### `GET /user/packages/{package_type}/{package_name}`
**Summary:** Get a package for the authenticated user
**Status:** planned

**Operations:**
- **read_one**
  - Component: `package`
  - Filters:
    - `package_type` eq `path.package_type`
    - `package_name` eq `path.package_name`
  - Notes:
    - Response body references #/components/schemas/package

#### `GET /users/{username}/packages`
**Summary:** List packages for a user
**Status:** planned

**Operations:**
- **read_one**
  - Component: `package`
  - Filters:
    - `username` eq `path.username`
  - Notes:
    - Query parameters: package_type

#### `GET /users/{username}/packages/{package_type}/{package_name}`
**Summary:** Get a package for a user
**Status:** planned

**Operations:**
- **read_one**
  - Component: `package`
  - Filters:
    - `username` eq `path.username`
    - `package_type` eq `path.package_type`
    - `package_name` eq `path.package_name`
  - Notes:
    - Response body references #/components/schemas/package
