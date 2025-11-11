# Component Plan: `empty-object`

**API Slug:** `github`
**Total Routes:** 21

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`update`**: Replace a full record.

## Routes

### GET Routes (1)

#### `GET /users/{username}/attestations/{subject_digest}`
**Summary:** List attestations
**Status:** planned

**Operations:**
- **read_one**
  - Component: `empty-object`
  - Filters:
    - `subject_digest` eq `path.subject_digest`
  - Notes:
    - Response body references #/components/schemas/empty-object
    - Query parameters: subject_digest

### POST Routes (11)

#### `POST /orgs/{org}/actions/variables`
**Summary:** Create an organization variable
**Status:** planned

**Operations:**
- **create**
  - Component: `empty-object`
  - Filters:
    - `org` eq `path.org`
  - Notes:
    - Response body references #/components/schemas/empty-object

#### `POST /repos/{owner}/{repo}/actions/jobs/{job_id}/rerun`
**Summary:** Re-run a job from a workflow run
**Status:** planned

**Operations:**
- **create**
  - Component: `empty-object`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `job_id` eq `path.job_id`
  - Notes:
    - Response body references #/components/schemas/empty-object

#### `POST /repos/{owner}/{repo}/actions/runs/{run_id}/approve`
**Summary:** Approve a workflow run for a fork pull request
**Status:** planned

**Operations:**
- **create**
  - Component: `empty-object`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `run_id` eq `path.run_id`
  - Notes:
    - Response body references #/components/schemas/empty-object

#### `POST /repos/{owner}/{repo}/actions/runs/{run_id}/cancel`
**Summary:** Cancel a workflow run
**Status:** planned

**Operations:**
- **create**
  - Component: `empty-object`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `run_id` eq `path.run_id`
  - Notes:
    - Response body references #/components/schemas/empty-object

#### `POST /repos/{owner}/{repo}/actions/runs/{run_id}/force-cancel`
**Summary:** Force cancel a workflow run
**Status:** planned

**Operations:**
- **create**
  - Component: `empty-object`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `run_id` eq `path.run_id`
  - Notes:
    - Response body references #/components/schemas/empty-object

#### `POST /repos/{owner}/{repo}/actions/runs/{run_id}/rerun`
**Summary:** Re-run a workflow
**Status:** planned

**Operations:**
- **create**
  - Component: `empty-object`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `run_id` eq `path.run_id`
  - Notes:
    - Response body references #/components/schemas/empty-object

#### `POST /repos/{owner}/{repo}/actions/runs/{run_id}/rerun-failed-jobs`
**Summary:** Re-run failed jobs from a workflow run
**Status:** planned

**Operations:**
- **create**
  - Component: `empty-object`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `run_id` eq `path.run_id`
  - Notes:
    - Response body references #/components/schemas/empty-object

#### `POST /repos/{owner}/{repo}/actions/variables`
**Summary:** Create a repository variable
**Status:** planned

**Operations:**
- **create**
  - Component: `empty-object`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/empty-object

#### `POST /repos/{owner}/{repo}/check-runs/{check_run_id}/rerequest`
**Summary:** Rerequest a check run
**Status:** planned

**Operations:**
- **create**
  - Component: `empty-object`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `check_run_id` eq `path.check_run_id`
  - Notes:
    - Response body references #/components/schemas/empty-object

#### `POST /repos/{owner}/{repo}/check-suites/{check_suite_id}/rerequest`
**Summary:** Rerequest a check suite
**Status:** planned

**Operations:**
- **create**
  - Component: `empty-object`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `check_suite_id` eq `path.check_suite_id`
  - Notes:
    - Response body references #/components/schemas/empty-object

#### `POST /repos/{owner}/{repo}/environments/{environment_name}/variables`
**Summary:** Create an environment variable
**Status:** planned

**Operations:**
- **create**
  - Component: `empty-object`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `environment_name` eq `path.environment_name`
  - Notes:
    - Response body references #/components/schemas/empty-object

### PUT Routes (9)

#### `PUT /orgs/{org}/actions/secrets/{secret_name}`
**Summary:** Create or update an organization secret
**Status:** planned

**Operations:**
- **update**
  - Component: `empty-object`
  - Filters:
    - `org` eq `path.org`
    - `secret_name` eq `path.secret_name`
  - Notes:
    - Response body references #/components/schemas/empty-object

#### `PUT /orgs/{org}/codespaces/secrets/{secret_name}`
**Summary:** Create or update an organization secret
**Status:** planned

**Operations:**
- **update**
  - Component: `empty-object`
  - Filters:
    - `org` eq `path.org`
    - `secret_name` eq `path.secret_name`
  - Notes:
    - Response body references #/components/schemas/empty-object

#### `PUT /orgs/{org}/dependabot/secrets/{secret_name}`
**Summary:** Create or update an organization secret
**Status:** planned

**Operations:**
- **update**
  - Component: `empty-object`
  - Filters:
    - `org` eq `path.org`
    - `secret_name` eq `path.secret_name`
  - Notes:
    - Response body references #/components/schemas/empty-object

#### `PUT /repos/{owner}/{repo}/actions/oidc/customization/sub`
**Summary:** Set the customization template for an OIDC subject claim for a repository
**Status:** planned

**Operations:**
- **update**
  - Component: `empty-object`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/empty-object

#### `PUT /repos/{owner}/{repo}/actions/secrets/{secret_name}`
**Summary:** Create or update a repository secret
**Status:** planned

**Operations:**
- **update**
  - Component: `empty-object`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `secret_name` eq `path.secret_name`
  - Notes:
    - Response body references #/components/schemas/empty-object

#### `PUT /repos/{owner}/{repo}/codespaces/secrets/{secret_name}`
**Summary:** Create or update a repository secret
**Status:** planned

**Operations:**
- **update**
  - Component: `empty-object`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `secret_name` eq `path.secret_name`
  - Notes:
    - Response body references #/components/schemas/empty-object

#### `PUT /repos/{owner}/{repo}/dependabot/secrets/{secret_name}`
**Summary:** Create or update a repository secret
**Status:** planned

**Operations:**
- **update**
  - Component: `empty-object`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `secret_name` eq `path.secret_name`
  - Notes:
    - Response body references #/components/schemas/empty-object

#### `PUT /repos/{owner}/{repo}/environments/{environment_name}/secrets/{secret_name}`
**Summary:** Create or update an environment secret
**Status:** planned

**Operations:**
- **update**
  - Component: `empty-object`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `environment_name` eq `path.environment_name`
    - `secret_name` eq `path.secret_name`
  - Notes:
    - Response body references #/components/schemas/empty-object

#### `PUT /user/codespaces/secrets/{secret_name}`
**Summary:** Create or update a secret for the authenticated user
**Status:** planned

**Operations:**
- **update**
  - Component: `empty-object`
  - Filters:
    - `secret_name` eq `path.secret_name`
  - Notes:
    - Response body references #/components/schemas/empty-object
