# Component Plan: `reaction`

**API Slug:** `github`
**Total Routes:** 25

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (7)

#### `DELETE /orgs/{org}/teams/{team_slug}/discussions/{discussion_number}/comments/{comment_number}/reactions/{reaction_id}`
**Summary:** Delete team discussion comment reaction
**Status:** planned

**Operations:**
- **delete**
  - Component: `reaction`
  - Filters:
    - `org` eq `path.org`
    - `team_slug` eq `path.team_slug`
    - `discussion_number` eq `path.discussion_number`
    - `comment_number` eq `path.comment_number`
    - `reaction_id` eq `path.reaction_id`

#### `DELETE /orgs/{org}/teams/{team_slug}/discussions/{discussion_number}/reactions/{reaction_id}`
**Summary:** Delete team discussion reaction
**Status:** planned

**Operations:**
- **delete**
  - Component: `reaction`
  - Filters:
    - `org` eq `path.org`
    - `team_slug` eq `path.team_slug`
    - `discussion_number` eq `path.discussion_number`
    - `reaction_id` eq `path.reaction_id`

#### `DELETE /repos/{owner}/{repo}/comments/{comment_id}/reactions/{reaction_id}`
**Summary:** Delete a commit comment reaction
**Status:** planned

**Operations:**
- **delete**
  - Component: `reaction`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `comment_id` eq `path.comment_id`
    - `reaction_id` eq `path.reaction_id`

#### `DELETE /repos/{owner}/{repo}/issues/comments/{comment_id}/reactions/{reaction_id}`
**Summary:** Delete an issue comment reaction
**Status:** planned

**Operations:**
- **delete**
  - Component: `reaction`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `comment_id` eq `path.comment_id`
    - `reaction_id` eq `path.reaction_id`

#### `DELETE /repos/{owner}/{repo}/issues/{issue_number}/reactions/{reaction_id}`
**Summary:** Delete an issue reaction
**Status:** planned

**Operations:**
- **delete**
  - Component: `reaction`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `issue_number` eq `path.issue_number`
    - `reaction_id` eq `path.reaction_id`

#### `DELETE /repos/{owner}/{repo}/pulls/comments/{comment_id}/reactions/{reaction_id}`
**Summary:** Delete a pull request comment reaction
**Status:** planned

**Operations:**
- **delete**
  - Component: `reaction`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `comment_id` eq `path.comment_id`
    - `reaction_id` eq `path.reaction_id`

#### `DELETE /repos/{owner}/{repo}/releases/{release_id}/reactions/{reaction_id}`
**Summary:** Delete a release reaction
**Status:** planned

**Operations:**
- **delete**
  - Component: `reaction`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `release_id` eq `path.release_id`
    - `reaction_id` eq `path.reaction_id`

### GET Routes (9)

#### `GET /orgs/{org}/teams/{team_slug}/discussions/{discussion_number}/comments/{comment_number}/reactions`
**Summary:** List reactions for a team discussion comment
**Status:** planned

**Operations:**
- **read_one**
  - Component: `reaction`
  - Filters:
    - `org` eq `path.org`
    - `team_slug` eq `path.team_slug`
    - `discussion_number` eq `path.discussion_number`
    - `comment_number` eq `path.comment_number`
  - Notes:
    - Query parameters: content

#### `GET /orgs/{org}/teams/{team_slug}/discussions/{discussion_number}/reactions`
**Summary:** List reactions for a team discussion
**Status:** planned

**Operations:**
- **read_one**
  - Component: `reaction`
  - Filters:
    - `org` eq `path.org`
    - `team_slug` eq `path.team_slug`
    - `discussion_number` eq `path.discussion_number`
  - Notes:
    - Query parameters: content

#### `GET /repos/{owner}/{repo}/comments/{comment_id}/reactions`
**Summary:** List reactions for a commit comment
**Status:** planned

**Operations:**
- **read_one**
  - Component: `reaction`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `comment_id` eq `path.comment_id`
  - Notes:
    - Query parameters: content

#### `GET /repos/{owner}/{repo}/issues/comments/{comment_id}/reactions`
**Summary:** List reactions for an issue comment
**Status:** planned

**Operations:**
- **read_one**
  - Component: `reaction`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `comment_id` eq `path.comment_id`
  - Notes:
    - Query parameters: content

#### `GET /repos/{owner}/{repo}/issues/{issue_number}/reactions`
**Summary:** List reactions for an issue
**Status:** planned

**Operations:**
- **read_one**
  - Component: `reaction`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `issue_number` eq `path.issue_number`
  - Notes:
    - Query parameters: content

#### `GET /repos/{owner}/{repo}/pulls/comments/{comment_id}/reactions`
**Summary:** List reactions for a pull request review comment
**Status:** planned

**Operations:**
- **read_one**
  - Component: `reaction`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `comment_id` eq `path.comment_id`
  - Notes:
    - Query parameters: content

#### `GET /repos/{owner}/{repo}/releases/{release_id}/reactions`
**Summary:** List reactions for a release
**Status:** planned

**Operations:**
- **read_one**
  - Component: `reaction`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `release_id` eq `path.release_id`
  - Notes:
    - Query parameters: content

#### `GET /teams/{team_id}/discussions/{discussion_number}/comments/{comment_number}/reactions`
**Summary:** List reactions for a team discussion comment (Legacy)
**Status:** planned

**Operations:**
- **read_one**
  - Component: `reaction`
  - Filters:
    - `team_id` eq `path.team_id`
    - `discussion_number` eq `path.discussion_number`
    - `comment_number` eq `path.comment_number`
  - Notes:
    - Query parameters: content

#### `GET /teams/{team_id}/discussions/{discussion_number}/reactions`
**Summary:** List reactions for a team discussion (Legacy)
**Status:** planned

**Operations:**
- **read_one**
  - Component: `reaction`
  - Filters:
    - `team_id` eq `path.team_id`
    - `discussion_number` eq `path.discussion_number`
  - Notes:
    - Query parameters: content

### POST Routes (9)

#### `POST /orgs/{org}/teams/{team_slug}/discussions/{discussion_number}/comments/{comment_number}/reactions`
**Summary:** Create reaction for a team discussion comment
**Status:** planned

**Operations:**
- **create**
  - Component: `reaction`
  - Filters:
    - `org` eq `path.org`
    - `team_slug` eq `path.team_slug`
    - `discussion_number` eq `path.discussion_number`
    - `comment_number` eq `path.comment_number`
  - Notes:
    - Response body references #/components/schemas/reaction

#### `POST /orgs/{org}/teams/{team_slug}/discussions/{discussion_number}/reactions`
**Summary:** Create reaction for a team discussion
**Status:** planned

**Operations:**
- **create**
  - Component: `reaction`
  - Filters:
    - `org` eq `path.org`
    - `team_slug` eq `path.team_slug`
    - `discussion_number` eq `path.discussion_number`
  - Notes:
    - Response body references #/components/schemas/reaction

#### `POST /repos/{owner}/{repo}/comments/{comment_id}/reactions`
**Summary:** Create reaction for a commit comment
**Status:** planned

**Operations:**
- **create**
  - Component: `reaction`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `comment_id` eq `path.comment_id`
  - Notes:
    - Response body references #/components/schemas/reaction

#### `POST /repos/{owner}/{repo}/issues/comments/{comment_id}/reactions`
**Summary:** Create reaction for an issue comment
**Status:** planned

**Operations:**
- **create**
  - Component: `reaction`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `comment_id` eq `path.comment_id`
  - Notes:
    - Response body references #/components/schemas/reaction

#### `POST /repos/{owner}/{repo}/issues/{issue_number}/reactions`
**Summary:** Create reaction for an issue
**Status:** planned

**Operations:**
- **create**
  - Component: `reaction`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `issue_number` eq `path.issue_number`
  - Notes:
    - Response body references #/components/schemas/reaction

#### `POST /repos/{owner}/{repo}/pulls/comments/{comment_id}/reactions`
**Summary:** Create reaction for a pull request review comment
**Status:** planned

**Operations:**
- **create**
  - Component: `reaction`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `comment_id` eq `path.comment_id`
  - Notes:
    - Response body references #/components/schemas/reaction

#### `POST /repos/{owner}/{repo}/releases/{release_id}/reactions`
**Summary:** Create reaction for a release
**Status:** planned

**Operations:**
- **create**
  - Component: `reaction`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `release_id` eq `path.release_id`
  - Notes:
    - Response body references #/components/schemas/reaction

#### `POST /teams/{team_id}/discussions/{discussion_number}/comments/{comment_number}/reactions`
**Summary:** Create reaction for a team discussion comment (Legacy)
**Status:** planned

**Operations:**
- **create**
  - Component: `reaction`
  - Filters:
    - `team_id` eq `path.team_id`
    - `discussion_number` eq `path.discussion_number`
    - `comment_number` eq `path.comment_number`
  - Notes:
    - Response body references #/components/schemas/reaction

#### `POST /teams/{team_id}/discussions/{discussion_number}/reactions`
**Summary:** Create reaction for a team discussion (Legacy)
**Status:** planned

**Operations:**
- **create**
  - Component: `reaction`
  - Filters:
    - `team_id` eq `path.team_id`
    - `discussion_number` eq `path.discussion_number`
  - Notes:
    - Response body references #/components/schemas/reaction
