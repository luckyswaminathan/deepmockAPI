# Component Plan: `code-scanning-codeql-database`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/code-scanning/codeql/databases/{language}`
**Summary:** Get a CodeQL database for a repository
**Status:** planned

**Operations:**
- **read_one**
  - Component: `code-scanning-codeql-database`
  - Filters:
    - `language` eq `path.language`
  - Notes:
    - Response body references #/components/schemas/code-scanning-codeql-database
    - Query parameters: language
