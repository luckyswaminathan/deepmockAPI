# Component Plan: `repository-ruleset`

**API Slug:** `github`
**Total Routes:** 6

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`update`**: Replace a full record.

## Routes

### GET Routes (2)

#### `GET /orgs/{org}/rulesets/{ruleset_id}`
**Summary:** Get an organization repository ruleset
**Status:** planned

**Operations:**
- **read_one**
  - Component: `repository-ruleset`
  - Filters:
    - `ruleset_id` eq `path.ruleset_id`
  - Notes:
    - Response body references #/components/schemas/repository-ruleset
    - Query parameters: ruleset_id

#### `GET /repos/{owner}/{repo}/rulesets/{ruleset_id}`
**Summary:** Get a repository ruleset
**Status:** planned

**Operations:**
- **read_one**
  - Component: `repository-ruleset`
  - Filters:
    - `ruleset_id` eq `path.ruleset_id`
  - Notes:
    - Response body references #/components/schemas/repository-ruleset
    - Query parameters: includes_parents

### POST Routes (2)

#### `POST /orgs/{org}/rulesets`
**Summary:** Create an organization repository ruleset
**Status:** planned

**Operations:**
- **create**
  - Component: `repository-ruleset`
  - Filters:
    - `org` eq `path.org`
  - Notes:
    - Response body references #/components/schemas/repository-ruleset

#### `POST /repos/{owner}/{repo}/rulesets`
**Summary:** Create a repository ruleset
**Status:** planned

**Operations:**
- **create**
  - Component: `repository-ruleset`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/repository-ruleset

### PUT Routes (2)

#### `PUT /orgs/{org}/rulesets/{ruleset_id}`
**Summary:** Update an organization repository ruleset
**Status:** planned

**Operations:**
- **update**
  - Component: `repository-ruleset`
  - Filters:
    - `ruleset_id` eq `path.ruleset_id`
  - Notes:
    - Response body references #/components/schemas/repository-ruleset
    - Query parameters: ruleset_id

#### `PUT /repos/{owner}/{repo}/rulesets/{ruleset_id}`
**Summary:** Update a repository ruleset
**Status:** planned

**Operations:**
- **update**
  - Component: `repository-ruleset`
  - Filters:
    - `ruleset_id` eq `path.ruleset_id`
  - Notes:
    - Response body references #/components/schemas/repository-ruleset
    - Query parameters: ruleset_id
