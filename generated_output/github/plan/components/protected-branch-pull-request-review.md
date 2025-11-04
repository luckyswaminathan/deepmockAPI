# Component Plan: `protected-branch-pull-request-review`

**API Slug:** `github`
**Total Routes:** 2

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.
- **`update_partial`**: Apply a partial update to a record.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/branches/{branch}/protection/required_pull_request_reviews`
**Summary:** Get pull request review protection
**Status:** planned

**Operations:**
- **read_one**
  - Component: `protected-branch-pull-request-review`
  - Filters:
    - `require_code_owner_reviews` eq `path.owner`
    - `repo` eq `path.repo`
    - `branch` eq `path.branch`
  - Notes:
    - Response body references #/components/schemas/protected-branch-pull-request-review

### PATCH Routes (1)

#### `PATCH /repos/{owner}/{repo}/branches/{branch}/protection/required_pull_request_reviews`
**Summary:** Update pull request review protection
**Status:** planned

**Operations:**
- **update_partial**
  - Component: `protected-branch-pull-request-review`
  - Filters:
    - `require_code_owner_reviews` eq `path.owner`
    - `repo` eq `path.repo`
    - `branch` eq `path.branch`
  - Notes:
    - Response body references #/components/schemas/protected-branch-pull-request-review
