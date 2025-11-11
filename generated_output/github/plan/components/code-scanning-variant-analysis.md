# Component Plan: `code-scanning-variant-analysis`

**API Slug:** `github`
**Total Routes:** 2

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/code-scanning/codeql/variant-analyses/{codeql_variant_analysis_id}`
**Summary:** Get the summary of a CodeQL variant analysis
**Status:** planned

**Operations:**
- **read_one**
  - Component: `code-scanning-variant-analysis`
  - Filters:
    - `codeql_variant_analysis_id` eq `path.codeql_variant_analysis_id`
  - Notes:
    - Response body references #/components/schemas/code-scanning-variant-analysis
    - Query parameters: codeql_variant_analysis_id

### POST Routes (1)

#### `POST /repos/{owner}/{repo}/code-scanning/codeql/variant-analyses`
**Summary:** Create a CodeQL variant analysis
**Status:** planned

**Operations:**
- **create**
  - Component: `code-scanning-variant-analysis`
  - Filters:
    - `owner` eq `path.owner`
    - `controller_repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/code-scanning-variant-analysis
