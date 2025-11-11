# Component Plan: `dependency-graph-spdx-sbom`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (1)

#### `GET /repos/{owner}/{repo}/dependency-graph/sbom`
**Summary:** Export a software bill of materials (SBOM) for a repository.
**Status:** planned

**Operations:**
- **read_one**
  - Component: `dependency-graph-spdx-sbom`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/dependency-graph-spdx-sbom
