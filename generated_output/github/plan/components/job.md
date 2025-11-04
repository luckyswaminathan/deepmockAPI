# Component Plan: `job`

**API Slug:** `github`
**Total Routes:** 3

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (3)

#### `GET /repos/{owner}/{repo}/actions/jobs/{job_id}`
**Summary:** Get a job for a workflow run
**Status:** planned

**Operations:**
- **read_one**
  - Component: `job`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `job_id` eq `path.job_id`
  - Notes:
    - Response body references #/components/schemas/job

#### `GET /repos/{owner}/{repo}/actions/runs/{run_id}/attempts/{attempt_number}/jobs`
**Summary:** List jobs for a workflow run attempt
**Status:** planned

**Operations:**
- **read_one**
  - Component: `job`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `run_id` eq `path.run_id`
    - `attempt_number` eq `path.attempt_number`

#### `GET /repos/{owner}/{repo}/actions/runs/{run_id}/jobs`
**Summary:** List jobs for a workflow run
**Status:** planned

**Operations:**
- **read_one**
  - Component: `job`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
    - `run_id` eq `path.run_id`
  - Notes:
    - Query parameters: filter
