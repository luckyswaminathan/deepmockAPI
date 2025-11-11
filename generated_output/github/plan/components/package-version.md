# Component Plan: `package-version`

**API Slug:** `github`
**Total Routes:** 3

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (3)

#### `GET /orgs/{org}/packages/{package_type}/{package_name}/versions/{package_version_id}`
**Summary:** Get a package version for an organization
**Status:** planned

**Operations:**
- **read_one**
  - Component: `package-version`
  - Filters:
    - `org` eq `path.org`
    - `package_type` eq `path.package_type`
    - `package_name` eq `path.package_name`
    - `package_version_id` eq `path.package_version_id`
  - Notes:
    - Response body references #/components/schemas/package-version

#### `GET /user/packages/{package_type}/{package_name}/versions/{package_version_id}`
**Summary:** Get a package version for the authenticated user
**Status:** planned

**Operations:**
- **read_one**
  - Component: `package-version`
  - Filters:
    - `package_type` eq `path.package_type`
    - `package_name` eq `path.package_name`
    - `package_version_id` eq `path.package_version_id`
  - Notes:
    - Response body references #/components/schemas/package-version

#### `GET /users/{username}/packages/{package_type}/{package_name}/versions/{package_version_id}`
**Summary:** Get a package version for a user
**Status:** planned

**Operations:**
- **read_one**
  - Component: `package-version`
  - Filters:
    - `username` eq `path.username`
    - `package_type` eq `path.package_type`
    - `package_name` eq `path.package_name`
    - `package_version_id` eq `path.package_version_id`
  - Notes:
    - Response body references #/components/schemas/package-version
