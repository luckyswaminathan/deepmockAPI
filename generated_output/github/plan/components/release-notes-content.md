# Component Plan: `release-notes-content`

**API Slug:** `github`
**Total Routes:** 1

## Supported Operations
- **`create`**: Create a new record for the component.

## Routes

### POST Routes (1)

#### `POST /repos/{owner}/{repo}/releases/generate-notes`
**Summary:** Generate release notes content for a release
**Status:** planned

**Operations:**
- **create**
  - Component: `release-notes-content`
  - Filters:
    - `owner` eq `path.owner`
    - `repo` eq `path.repo`
  - Notes:
    - Response body references #/components/schemas/release-notes-content
