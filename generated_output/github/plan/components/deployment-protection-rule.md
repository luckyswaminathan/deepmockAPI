# Component Plan: `deployment-protection-rule`

**API Slug:** `github`
**Total Routes:** 2

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/environments/{environment_name}/deployment_protection_rules/{protection_rule_id}`
**Summary:** Get a custom deployment protection rule
**Status:** planned

**Operations:**
- **read_one**
  - Component: `deployment-protection-rule`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `environment_name` eq `path.environment_name`
    - `protection_rule_id` eq `path.protection_rule_id`
  - Notes:
    - Response body references #/components/schemas/deployment-protection-rule

### POST Routes (1)

#### `POST /repos/{owner}/{repo}/environments/{environment_name}/deployment_protection_rules`
**Summary:** Create a custom deployment protection rule on an environment
**Status:** planned

**Operations:**
- **create**
  - Component: `deployment-protection-rule`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `environment_name` eq `path.environment_name`
  - Notes:
    - Response body references #/components/schemas/deployment-protection-rule
