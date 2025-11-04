# Component Plan: `code-scanning-variant-analysis-repo-task`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/code-scanning/codeql/variant-analyses/{codeql_variant_analysis_id}/repos/{repo_owner}/{repo_name}`
**Summary:** Get the analysis status of a repository in a CodeQL variant analysis
**Status:** planned

**Operations:**
- **read_one**
  - Component: `code-scanning-variant-analysis-repo-task`
  - Filters:
    - `repository` eq `path.repo`
    - `codeql_variant_analysis_id` eq `path.codeql_variant_analysis_id`
    - `repo_owner` eq `path.repo_owner`
    - `repo_name` eq `path.repo_name`
  - Notes:
    - Response body references #/components/schemas/code-scanning-variant-analysis-repo-task
    - Query parameters: repo, codeql_variant_analysis_id, repo_owner, repo_name
