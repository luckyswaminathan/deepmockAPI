# Component Plan: `team-discussion-comment`

**API Slug:** `github`
**Total Routes:** 6

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`update_partial`**: Apply a partial update to a record.

## Routes

### GET Routes (2)

#### `GET /orgs/{org}/teams/{team_slug}/discussions/{discussion_number}/comments/{comment_number}`
**Summary:** Get a discussion comment
**Status:** planned

**Operations:**
- **read_one**
  - Component: `team-discussion-comment`
  - Filters:
    - `org` eq `path.org`
    - `team_slug` eq `path.team_slug`
    - `discussion_number` eq `path.discussion_number`
    - `comment_number` eq `path.comment_number`
  - Notes:
    - Response body references #/components/schemas/team-discussion-comment

#### `GET /teams/{team_id}/discussions/{discussion_number}/comments/{comment_number}`
**Summary:** Get a discussion comment (Legacy)
**Status:** planned

**Operations:**
- **read_one**
  - Component: `team-discussion-comment`
  - Filters:
    - `team_id` eq `path.team_id`
    - `discussion_number` eq `path.discussion_number`
    - `comment_number` eq `path.comment_number`
  - Notes:
    - Response body references #/components/schemas/team-discussion-comment

### PATCH Routes (2)

#### `PATCH /orgs/{org}/teams/{team_slug}/discussions/{discussion_number}/comments/{comment_number}`
**Summary:** Update a discussion comment
**Status:** planned

**Operations:**
- **update_partial**
  - Component: `team-discussion-comment`
  - Filters:
    - `org` eq `path.org`
    - `team_slug` eq `path.team_slug`
    - `discussion_number` eq `path.discussion_number`
    - `comment_number` eq `path.comment_number`
  - Notes:
    - Response body references #/components/schemas/team-discussion-comment

#### `PATCH /teams/{team_id}/discussions/{discussion_number}/comments/{comment_number}`
**Summary:** Update a discussion comment (Legacy)
**Status:** planned

**Operations:**
- **update_partial**
  - Component: `team-discussion-comment`
  - Filters:
    - `team_id` eq `path.team_id`
    - `discussion_number` eq `path.discussion_number`
    - `comment_number` eq `path.comment_number`
  - Notes:
    - Response body references #/components/schemas/team-discussion-comment

### POST Routes (2)

#### `POST /orgs/{org}/teams/{team_slug}/discussions/{discussion_number}/comments`
**Summary:** Create a discussion comment
**Status:** planned

**Operations:**
- **create**
  - Component: `team-discussion-comment`
  - Filters:
    - `org` eq `path.org`
    - `team_slug` eq `path.team_slug`
    - `discussion_number` eq `path.discussion_number`
  - Notes:
    - Response body references #/components/schemas/team-discussion-comment

#### `POST /teams/{team_id}/discussions/{discussion_number}/comments`
**Summary:** Create a discussion comment (Legacy)
**Status:** planned

**Operations:**
- **create**
  - Component: `team-discussion-comment`
  - Filters:
    - `team_id` eq `path.team_id`
    - `discussion_number` eq `path.discussion_number`
  - Notes:
    - Response body references #/components/schemas/team-discussion-comment
