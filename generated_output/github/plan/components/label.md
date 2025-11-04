# Component Plan: `label`

**API Slug:** `github`
**Total Routes:** 22

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.
- **`update`**: Replace a full record.
- **`update_partial`**: Apply a partial update to a record.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (7)

#### `DELETE /orgs/{org}/actions/runners/{runner_id}/labels`
**Summary:** Remove all custom labels from a self-hosted runner for an organization
**Status:** planned

**Operations:**
- **delete**
  - Component: `label`
  - Filters:
    - `org` eq `path.org`
    - `runner_id` eq `path.runner_id`

#### `DELETE /orgs/{org}/actions/runners/{runner_id}/labels/{name}`
**Summary:** Remove a custom label from a self-hosted runner for an organization
**Status:** planned

**Operations:**
- **delete**
  - Component: `label`
  - Filters:
    - `org` eq `path.org`
    - `runner_id` eq `path.runner_id`
    - `name` eq `path.name`

#### `DELETE /repos/{owner}/{repo}/actions/runners/{runner_id}/labels`
**Summary:** Remove all custom labels from a self-hosted runner for a repository
**Status:** planned

**Operations:**
- **delete**
  - Component: `label`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `runner_id` eq `path.runner_id`

#### `DELETE /repos/{owner}/{repo}/actions/runners/{runner_id}/labels/{name}`
**Summary:** Remove a custom label from a self-hosted runner for a repository
**Status:** planned

**Operations:**
- **delete**
  - Component: `label`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `runner_id` eq `path.runner_id`
    - `name` eq `path.name`

#### `DELETE /repos/{owner}/{repo}/issues/{issue_number}/labels`
**Summary:** Remove all labels from an issue
**Status:** planned

**Operations:**
- **delete**
  - Component: `label`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `issue_number` eq `path.issue_number`

#### `DELETE /repos/{owner}/{repo}/issues/{issue_number}/labels/{name}`
**Summary:** Remove a label from an issue
**Status:** planned

**Operations:**
- **delete**
  - Component: `label`
  - Filters:
    - `name` eq `path.name`
  - Notes:
    - Query parameters: name

#### `DELETE /repos/{owner}/{repo}/labels/{name}`
**Summary:** Delete a label
**Status:** planned

**Operations:**
- **delete**
  - Component: `label`
  - Filters:
    - `name` eq `path.name`
  - Notes:
    - Query parameters: name

### GET Routes (7)

#### `GET /orgs/{org}/actions/runners/{runner_id}/labels`
**Summary:** List labels for a self-hosted runner for an organization
**Status:** planned

**Operations:**
- **read_one**
  - Component: `label`
  - Filters:
    - `org` eq `path.org`
    - `runner_id` eq `path.runner_id`

#### `GET /repos/{owner}/{repo}/actions/runners/{runner_id}/labels`
**Summary:** List labels for a self-hosted runner for a repository
**Status:** planned

**Operations:**
- **read_one**
  - Component: `label`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `runner_id` eq `path.runner_id`

#### `GET /repos/{owner}/{repo}/issues/{issue_number}/labels`
**Summary:** List labels for an issue
**Status:** planned

**Operations:**
- **read_one**
  - Component: `label`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `issue_number` eq `path.issue_number`

#### `GET /repos/{owner}/{repo}/labels`
**Summary:** List labels for a repository
**Status:** planned

**Operations:**
- **read_one**
  - Component: `label`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`

#### `GET /repos/{owner}/{repo}/labels/{name}`
**Summary:** Get a label
**Status:** planned

**Operations:**
- **read_one**
  - Component: `label`
  - Filters:
    - `name` eq `path.name`
  - Notes:
    - Response body references #/components/schemas/label
    - Query parameters: name

#### `GET /repos/{owner}/{repo}/milestones/{milestone_number}/labels`
**Summary:** List labels for issues in a milestone
**Status:** planned

**Operations:**
- **read_one**
  - Component: `label`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `milestone_number` eq `path.milestone_number`

#### `GET /search/labels`
**Summary:** Search labels
**Status:** planned

**Operations:**
- **read_many**
  - Component: `label`
  - Notes:
    - Query parameters: repository_id, q, sort

### PATCH Routes (1)

#### `PATCH /repos/{owner}/{repo}/labels/{name}`
**Summary:** Update a label
**Status:** planned

**Operations:**
- **update_partial**
  - Component: `label`
  - Filters:
    - `name` eq `path.name`
  - Notes:
    - Response body references #/components/schemas/label
    - Query parameters: name

### POST Routes (4)

#### `POST /orgs/{org}/actions/runners/{runner_id}/labels`
**Summary:** Add custom labels to a self-hosted runner for an organization
**Status:** planned

**Operations:**
- **create**
  - Component: `label`
  - Filters:
    - `org` eq `path.org`
    - `runner_id` eq `path.runner_id`

#### `POST /repos/{owner}/{repo}/actions/runners/{runner_id}/labels`
**Summary:** Add custom labels to a self-hosted runner for a repository
**Status:** planned

**Operations:**
- **create**
  - Component: `label`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `runner_id` eq `path.runner_id`

#### `POST /repos/{owner}/{repo}/issues/{issue_number}/labels`
**Summary:** Add labels to an issue
**Status:** planned

**Operations:**
- **create**
  - Component: `label`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `issue_number` eq `path.issue_number`

#### `POST /repos/{owner}/{repo}/labels`
**Summary:** Create a label
**Status:** planned

**Operations:**
- **create**
  - Component: `label`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/label

### PUT Routes (3)

#### `PUT /orgs/{org}/actions/runners/{runner_id}/labels`
**Summary:** Set custom labels for a self-hosted runner for an organization
**Status:** planned

**Operations:**
- **update**
  - Component: `label`
  - Filters:
    - `org` eq `path.org`
    - `runner_id` eq `path.runner_id`

#### `PUT /repos/{owner}/{repo}/actions/runners/{runner_id}/labels`
**Summary:** Set custom labels for a self-hosted runner for a repository
**Status:** planned

**Operations:**
- **update**
  - Component: `label`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `runner_id` eq `path.runner_id`

#### `PUT /repos/{owner}/{repo}/issues/{issue_number}/labels`
**Summary:** Set labels for an issue
**Status:** planned

**Operations:**
- **update**
  - Component: `label`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `issue_number` eq `path.issue_number`
