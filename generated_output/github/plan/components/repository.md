# Component Plan: `repository`

**API Slug:** `github`
**Total Routes:** 45

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.
- **`update`**: Replace a full record.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (10)

#### `DELETE /orgs/{org}/actions/permissions/repositories/{repository_id}`
**Summary:** Disable a selected repository for GitHub Actions in an organization
**Status:** planned

**Operations:**
- **delete**
  - Component: `repository`
  - Filters:
    - `org` eq `path.org`
    - `repository_id` eq `path.repository_id`

#### `DELETE /orgs/{org}/actions/secrets/{secret_name}/repositories/{repository_id}`
**Summary:** Remove selected repository from an organization secret
**Status:** planned

**Operations:**
- **delete**
  - Component: `repository`
  - Filters:
    - `repository_id` eq `path.repository_id`
  - Notes:
    - Query parameters: repository_id

#### `DELETE /orgs/{org}/actions/variables/{name}/repositories/{repository_id}`
**Summary:** Remove selected repository from an organization variable
**Status:** planned

**Operations:**
- **delete**
  - Component: `repository`
  - Filters:
    - `repository_id` eq `path.repository_id`
  - Notes:
    - Query parameters: repository_id

#### `DELETE /orgs/{org}/codespaces/secrets/{secret_name}/repositories/{repository_id}`
**Summary:** Remove selected repository from an organization secret
**Status:** planned

**Operations:**
- **delete**
  - Component: `repository`
  - Filters:
    - `repository_id` eq `path.repository_id`
  - Notes:
    - Query parameters: repository_id

#### `DELETE /orgs/{org}/dependabot/secrets/{secret_name}/repositories/{repository_id}`
**Summary:** Remove selected repository from an organization secret
**Status:** planned

**Operations:**
- **delete**
  - Component: `repository`
  - Filters:
    - `repository_id` eq `path.repository_id`
  - Notes:
    - Query parameters: repository_id

#### `DELETE /orgs/{org}/teams/{team_slug}/repos/{owner}/{repo}`
**Summary:** Remove a repository from a team
**Status:** planned

**Operations:**
- **delete**
  - Component: `repository`
  - Filters:
    - `org` eq `path.org`
    - `team_slug` eq `path.team_slug`
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`

#### `DELETE /repos/{owner}/{repo}`
**Summary:** Delete a repository
**Status:** planned

**Operations:**
- **delete**
  - Component: `repository`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`

#### `DELETE /teams/{team_id}/repos/{owner}/{repo}`
**Summary:** Remove a repository from a team (Legacy)
**Status:** planned

**Operations:**
- **delete**
  - Component: `repository`
  - Filters:
    - `team_id` eq `path.team_id`
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`

#### `DELETE /user/codespaces/secrets/{secret_name}/repositories/{repository_id}`
**Summary:** Remove a selected repository from a user secret
**Status:** planned

**Operations:**
- **delete**
  - Component: `repository`
  - Filters:
    - `repository_id` eq `path.repository_id`
  - Notes:
    - Query parameters: repository_id

#### `DELETE /user/installations/{installation_id}/repositories/{repository_id}`
**Summary:** Remove a repository from an app installation
**Status:** planned

**Operations:**
- **delete**
  - Component: `repository`
  - Filters:
    - `installation_id` eq `path.installation_id`
    - `repository_id` eq `path.repository_id`

### GET Routes (20)

#### `GET /installation/repositories`
**Summary:** List repositories accessible to the app installation
**Status:** planned

**Operations:**
- **read_many**
  - Component: `repository`

#### `GET /orgs/{org}/actions/permissions/repositories`
**Summary:** List selected repositories enabled for GitHub Actions in an organization
**Status:** planned

**Operations:**
- **read_one**
  - Component: `repository`
  - Filters:
    - `org` eq `path.org`

#### `GET /orgs/{org}/actions/secrets/{secret_name}/repositories`
**Summary:** List selected repositories for an organization secret
**Status:** planned

**Operations:**
- **read_one**
  - Component: `repository`
  - Filters:
    - `org` eq `path.org`
    - `secret_name` eq `path.secret_name`

#### `GET /orgs/{org}/actions/variables/{name}/repositories`
**Summary:** List selected repositories for an organization variable
**Status:** planned

**Operations:**
- **read_one**
  - Component: `repository`
  - Filters:
    - `org` eq `path.org`
    - `name` eq `path.name`

#### `GET /orgs/{org}/code-security/configurations/{configuration_id}/repositories`
**Summary:** Get repositories associated with a code security configuration
**Status:** planned

**Operations:**
- **read_one**
  - Component: `repository`
  - Filters:
    - `org` eq `path.org`
    - `configuration_id` eq `path.configuration_id`
  - Notes:
    - Query parameters: per_page, status

#### `GET /orgs/{org}/codespaces/secrets/{secret_name}/repositories`
**Summary:** List selected repositories for an organization secret
**Status:** planned

**Operations:**
- **read_one**
  - Component: `repository`
  - Filters:
    - `org` eq `path.org`
    - `secret_name` eq `path.secret_name`

#### `GET /orgs/{org}/dependabot/secrets/{secret_name}/repositories`
**Summary:** List selected repositories for an organization secret
**Status:** planned

**Operations:**
- **read_one**
  - Component: `repository`
  - Filters:
    - `org` eq `path.org`
    - `secret_name` eq `path.secret_name`

#### `GET /orgs/{org}/migrations/{migration_id}/repositories`
**Summary:** List repositories in an organization migration
**Status:** planned

**Operations:**
- **read_one**
  - Component: `repository`
  - Filters:
    - `org` eq `path.org`
    - `migration_id` eq `path.migration_id`

#### `GET /orgs/{org}/personal-access-token-requests/{pat_request_id}/repositories`
**Summary:** List repositories requested to be accessed by a fine-grained personal access token
**Status:** planned

**Operations:**
- **read_one**
  - Component: `repository`
  - Filters:
    - `pat_request_id` eq `path.pat_request_id`
  - Notes:
    - Query parameters: pat_request_id

#### `GET /orgs/{org}/personal-access-tokens/{pat_id}/repositories`
**Summary:** List repositories a fine-grained personal access token has access to
**Status:** planned

**Operations:**
- **read_one**
  - Component: `repository`
  - Filters:
    - `pat_id` eq `path.pat_id`
  - Notes:
    - Query parameters: pat_id

#### `GET /orgs/{org}/repos`
**Summary:** List organization repositories
**Status:** planned

**Operations:**
- **read_one**
  - Component: `repository`
  - Filters:
    - `org` eq `path.org`
  - Notes:
    - Query parameters: type, sort, direction

#### `GET /orgs/{org}/teams/{team_slug}/repos`
**Summary:** List team repositories
**Status:** planned

**Operations:**
- **read_one**
  - Component: `repository`
  - Filters:
    - `org` eq `path.org`
    - `team_slug` eq `path.team_slug`

#### `GET /repositories`
**Summary:** List public repositories
**Status:** planned

**Operations:**
- **read_many**
  - Component: `repository`

#### `GET /search/repositories`
**Summary:** Search repositories
**Status:** planned

**Operations:**
- **read_many**
  - Component: `repository`
  - Notes:
    - Query parameters: q, sort

#### `GET /teams/{team_id}/repos`
**Summary:** List team repositories (Legacy)
**Status:** planned

**Operations:**
- **read_one**
  - Component: `repository`
  - Filters:
    - `team_id` eq `path.team_id`

#### `GET /user/codespaces/secrets/{secret_name}/repositories`
**Summary:** List selected repositories for a user secret
**Status:** planned

**Operations:**
- **read_one**
  - Component: `repository`
  - Filters:
    - `secret_name` eq `path.secret_name`

#### `GET /user/installations/{installation_id}/repositories`
**Summary:** List repositories accessible to the user access token
**Status:** planned

**Operations:**
- **read_one**
  - Component: `repository`
  - Filters:
    - `installation_id` eq `path.installation_id`

#### `GET /user/migrations/{migration_id}/repositories`
**Summary:** List repositories for a user migration
**Status:** planned

**Operations:**
- **read_one**
  - Component: `repository`
  - Filters:
    - `migration_id` eq `path.migration_id`

#### `GET /user/repos`
**Summary:** List repositories for the authenticated user
**Status:** planned

**Operations:**
- **read_many**
  - Component: `repository`
  - Notes:
    - Query parameters: visibility, affiliation, type, sort, direction

#### `GET /users/{username}/repos`
**Summary:** List repositories for a user
**Status:** planned

**Operations:**
- **read_one**
  - Component: `repository`
  - Filters:
    - `username` eq `path.username`
  - Notes:
    - Query parameters: type, sort, direction

### PUT Routes (15)

#### `PUT /orgs/{org}/actions/permissions/repositories`
**Summary:** Set selected repositories enabled for GitHub Actions in an organization
**Status:** planned

**Operations:**
- **update**
  - Component: `repository`
  - Filters:
    - `org` eq `path.org`

#### `PUT /orgs/{org}/actions/permissions/repositories/{repository_id}`
**Summary:** Enable a selected repository for GitHub Actions in an organization
**Status:** planned

**Operations:**
- **update**
  - Component: `repository`
  - Filters:
    - `org` eq `path.org`
    - `repository_id` eq `path.repository_id`

#### `PUT /orgs/{org}/actions/secrets/{secret_name}/repositories`
**Summary:** Set selected repositories for an organization secret
**Status:** planned

**Operations:**
- **update**
  - Component: `repository`
  - Filters:
    - `org` eq `path.org`
    - `secret_name` eq `path.secret_name`

#### `PUT /orgs/{org}/actions/secrets/{secret_name}/repositories/{repository_id}`
**Summary:** Add selected repository to an organization secret
**Status:** planned

**Operations:**
- **update**
  - Component: `repository`
  - Filters:
    - `repository_id` eq `path.repository_id`
  - Notes:
    - Query parameters: repository_id

#### `PUT /orgs/{org}/actions/variables/{name}/repositories`
**Summary:** Set selected repositories for an organization variable
**Status:** planned

**Operations:**
- **update**
  - Component: `repository`
  - Filters:
    - `org` eq `path.org`
    - `name` eq `path.name`

#### `PUT /orgs/{org}/actions/variables/{name}/repositories/{repository_id}`
**Summary:** Add selected repository to an organization variable
**Status:** planned

**Operations:**
- **update**
  - Component: `repository`
  - Filters:
    - `repository_id` eq `path.repository_id`
  - Notes:
    - Query parameters: repository_id

#### `PUT /orgs/{org}/codespaces/secrets/{secret_name}/repositories`
**Summary:** Set selected repositories for an organization secret
**Status:** planned

**Operations:**
- **update**
  - Component: `repository`
  - Filters:
    - `org` eq `path.org`
    - `secret_name` eq `path.secret_name`

#### `PUT /orgs/{org}/codespaces/secrets/{secret_name}/repositories/{repository_id}`
**Summary:** Add selected repository to an organization secret
**Status:** planned

**Operations:**
- **update**
  - Component: `repository`
  - Filters:
    - `repository_id` eq `path.repository_id`
  - Notes:
    - Query parameters: repository_id

#### `PUT /orgs/{org}/dependabot/secrets/{secret_name}/repositories`
**Summary:** Set selected repositories for an organization secret
**Status:** planned

**Operations:**
- **update**
  - Component: `repository`
  - Filters:
    - `org` eq `path.org`
    - `secret_name` eq `path.secret_name`

#### `PUT /orgs/{org}/dependabot/secrets/{secret_name}/repositories/{repository_id}`
**Summary:** Add selected repository to an organization secret
**Status:** planned

**Operations:**
- **update**
  - Component: `repository`
  - Filters:
    - `repository_id` eq `path.repository_id`
  - Notes:
    - Query parameters: repository_id

#### `PUT /orgs/{org}/teams/{team_slug}/repos/{owner}/{repo}`
**Summary:** Add or update team repository permissions
**Status:** planned

**Operations:**
- **update**
  - Component: `repository`
  - Filters:
    - `org` eq `path.org`
    - `team_slug` eq `path.team_slug`
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`

#### `PUT /teams/{team_id}/repos/{owner}/{repo}`
**Summary:** Add or update team repository permissions (Legacy)
**Status:** planned

**Operations:**
- **update**
  - Component: `repository`
  - Filters:
    - `team_id` eq `path.team_id`
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`

#### `PUT /user/codespaces/secrets/{secret_name}/repositories`
**Summary:** Set selected repositories for a user secret
**Status:** planned

**Operations:**
- **update**
  - Component: `repository`
  - Filters:
    - `secret_name` eq `path.secret_name`

#### `PUT /user/codespaces/secrets/{secret_name}/repositories/{repository_id}`
**Summary:** Add a selected repository to a user secret
**Status:** planned

**Operations:**
- **update**
  - Component: `repository`
  - Filters:
    - `repository_id` eq `path.repository_id`
  - Notes:
    - Query parameters: repository_id

#### `PUT /user/installations/{installation_id}/repositories/{repository_id}`
**Summary:** Add a repository to an app installation
**Status:** planned

**Operations:**
- **update**
  - Component: `repository`
  - Filters:
    - `installation_id` eq `path.installation_id`
    - `repository_id` eq `path.repository_id`
