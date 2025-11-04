# Component Plan: `rule-suites`

**API Slug:** `github`
**Total Routes:** 2

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (2)

#### `GET /orgs/{org}/rulesets/rule-suites`
**Summary:** List organization rule suites
**Status:** planned

**Operations:**
- **read_one**
  - Component: `rule-suites`
  - Filters:
    - `org` eq `path.org`
  - Notes:
    - Response body references #/components/schemas/rule-suites

#### `GET /repos/{owner}/{repo}/rulesets/rule-suites`
**Summary:** List repository rule suites
**Status:** planned

**Operations:**
- **read_one**
  - Component: `rule-suites`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/rule-suites
