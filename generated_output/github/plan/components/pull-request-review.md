# Component Plan: `pull-request-review`

**API Slug:** `github`
**Total Routes:** 6

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`update`**: Replace a full record.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (1)

#### `DELETE /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`
**Summary:** Delete a pending review for a pull request
**Status:** planned

**Operations:**
- **delete**
  - Component: `pull-request-review`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `pull_number` eq `path.pull_number`
    - `review_id` eq `path.review_id`
  - Notes:
    - Response body references #/components/schemas/pull-request-review

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`
**Summary:** Get a review for a pull request
**Status:** planned

**Operations:**
- **read_one**
  - Component: `pull-request-review`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `pull_number` eq `path.pull_number`
    - `review_id` eq `path.review_id`
  - Notes:
    - Response body references #/components/schemas/pull-request-review

### POST Routes (2)

#### `POST /repos/{owner}/{repo}/pulls/{pull_number}/reviews`
**Summary:** Create a review for a pull request
**Status:** planned

**Operations:**
- **create**
  - Component: `pull-request-review`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `pull_number` eq `path.pull_number`
  - Notes:
    - Response body references #/components/schemas/pull-request-review

#### `POST /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}/events`
**Summary:** Submit a review for a pull request
**Status:** planned

**Operations:**
- **create**
  - Component: `pull-request-review`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `pull_number` eq `path.pull_number`
    - `review_id` eq `path.review_id`
  - Notes:
    - Response body references #/components/schemas/pull-request-review

### PUT Routes (2)

#### `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}`
**Summary:** Update a review for a pull request
**Status:** planned

**Operations:**
- **update**
  - Component: `pull-request-review`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `pull_number` eq `path.pull_number`
    - `review_id` eq `path.review_id`
  - Notes:
    - Response body references #/components/schemas/pull-request-review

#### `PUT /repos/{owner}/{repo}/pulls/{pull_number}/reviews/{review_id}/dismissals`
**Summary:** Dismiss a review for a pull request
**Status:** planned

**Operations:**
- **update**
  - Component: `pull-request-review`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `pull_number` eq `path.pull_number`
    - `review_id` eq `path.review_id`
  - Notes:
    - Response body references #/components/schemas/pull-request-review
