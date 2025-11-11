# Component Plan: `code-scanning-analysis-deletion`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (1)

#### `DELETE /repos/{owner}/{repo}/code-scanning/analyses/{analysis_id}`
**Summary:** Delete a code scanning analysis from a repository
**Status:** planned

**Operations:**
- **delete**
  - Component: `code-scanning-analysis-deletion`
  - Filters:
    - `analysis_id` eq `path.analysis_id`
  - Notes:
    - Response body references #/components/schemas/code-scanning-analysis-deletion
    - Query parameters: confirm_delete
