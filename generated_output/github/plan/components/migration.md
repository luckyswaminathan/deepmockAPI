# Component Plan: `migration`

**API Slug:** `github`
**Total Routes:** 6

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.

## Routes

### GET Routes (4)

#### `GET /orgs/{org}/migrations`
**Summary:** List organization migrations
**Status:** planned

**Operations:**
- **read_one**
  - Component: `migration`
  - Filters:
    - `org` eq `path.org`
  - Notes:
    - Query parameters: exclude

#### `GET /orgs/{org}/migrations/{migration_id}`
**Summary:** Get an organization migration status
**Status:** planned

**Operations:**
- **read_one**
  - Component: `migration`
  - Filters:
    - `org` eq `path.org`
    - `migration_id` eq `path.migration_id`
  - Notes:
    - Response body references #/components/schemas/migration
    - Query parameters: exclude

#### `GET /user/migrations`
**Summary:** List user migrations
**Status:** planned

**Operations:**
- **read_many**
  - Component: `migration`

#### `GET /user/migrations/{migration_id}`
**Summary:** Get a user migration status
**Status:** planned

**Operations:**
- **read_one**
  - Component: `migration`
  - Filters:
    - `migration_id` eq `path.migration_id`
  - Notes:
    - Response body references #/components/schemas/migration
    - Query parameters: exclude

### POST Routes (2)

#### `POST /orgs/{org}/migrations`
**Summary:** Start an organization migration
**Status:** planned

**Operations:**
- **create**
  - Component: `migration`
  - Filters:
    - `org` eq `path.org`
  - Notes:
    - Response body references #/components/schemas/migration

#### `POST /user/migrations`
**Summary:** Start a user migration
**Status:** planned

**Operations:**
- **create**
  - Component: `migration`
  - Notes:
    - Response body references #/components/schemas/migration
