# Component Plan: `locked-issue-event`

**API Slug:** `github`
**Total Routes:** 4

## Supported Operations
- **`update`**: Replace a full record.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (3)

#### `DELETE /orgs/{org}/migrations/{migration_id}/repos/{repo_name}/lock`
**Summary:** Unlock an organization repository
**Status:** planned

**Operations:**
- **delete**
  - Component: `locked-issue-event`
  - Filters:
    - `org` eq `path.org`
    - `migration_id` eq `path.migration_id`
    - `repo_name` eq `path.repo_name`

#### `DELETE /repos/{owner}/{repo}/issues/{issue_number}/lock`
**Summary:** Unlock an issue
**Status:** planned

**Operations:**
- **delete**
  - Component: `locked-issue-event`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `issue_number` eq `path.issue_number`

#### `DELETE /user/migrations/{migration_id}/repos/{repo_name}/lock`
**Summary:** Unlock a user repository
**Status:** planned

**Operations:**
- **delete**
  - Component: `locked-issue-event`
  - Filters:
    - `migration_id` eq `path.migration_id`
    - `repo_name` eq `path.repo_name`

### PUT Routes (1)

#### `PUT /repos/{owner}/{repo}/issues/{issue_number}/lock`
**Summary:** Lock an issue
**Status:** planned

**Operations:**
- **update**
  - Component: `locked-issue-event`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `issue_number` eq `path.issue_number`
