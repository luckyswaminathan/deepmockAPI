# Component Plan: `timeline-assigned-issue-event`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/issues/{issue_number}/timeline`
**Summary:** List timeline events for an issue
**Status:** planned

**Operations:**
- **read_one**
  - Component: `timeline-assigned-issue-event`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `issue_number` eq `path.issue_number`
