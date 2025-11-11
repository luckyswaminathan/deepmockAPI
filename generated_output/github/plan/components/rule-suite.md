# Component Plan: `rule-suite`

**API Slug:** `github`
**Total Routes:** 2

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (2)

#### `GET /orgs/{org}/rulesets/rule-suites/{rule_suite_id}`
**Summary:** Get an organization rule suite
**Status:** planned

**Operations:**
- **read_one**
  - Component: `rule-suite`
  - Filters:
    - `org` eq `path.org`
    - `rule_suite_id` eq `path.rule_suite_id`
  - Notes:
    - Response body references #/components/schemas/rule-suite

#### `GET /repos/{owner}/{repo}/rulesets/rule-suites/{rule_suite_id}`
**Summary:** Get a repository rule suite
**Status:** planned

**Operations:**
- **read_one**
  - Component: `rule-suite`
  - Filters:
    - `owner` eq `path.owner`
    - `repository_id` eq `path.repo`
    - `rule_suite_id` eq `path.rule_suite_id`
  - Notes:
    - Response body references #/components/schemas/rule-suite
