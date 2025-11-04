# Component Plan: `hook-delivery`

**API Slug:** `github`
**Total Routes:** 3

## Supported Operations
- **`read_one`**: Fetch a single record by identifier.

## Routes

### GET Routes (3)

#### `GET /app/hook/deliveries/{delivery_id}`
**Summary:** Get a delivery for an app webhook
**Status:** planned

**Operations:**
- **read_one**
  - Component: `hook-delivery`
  - Filters:
    - `delivery_id` eq `path.delivery_id`
  - Notes:
    - Response body references #/components/schemas/hook-delivery

#### `GET /orgs/{org}/hooks/{hook_id}/deliveries/{delivery_id}`
**Summary:** Get a webhook delivery for an organization webhook
**Status:** planned

**Operations:**
- **read_one**
  - Component: `hook-delivery`
  - Filters:
    - `org` eq `path.org`
    - `hook_id` eq `path.hook_id`
    - `delivery_id` eq `path.delivery_id`
  - Notes:
    - Response body references #/components/schemas/hook-delivery

#### `GET /repos/{owner}/{repo}/hooks/{hook_id}/deliveries/{delivery_id}`
**Summary:** Get a delivery for a repository webhook
**Status:** planned

**Operations:**
- **read_one**
  - Component: `hook-delivery`
  - Filters:
    - `owner` eq `path.owner`
    - `repository_id` eq `path.repo`
    - `hook_id` eq `path.hook_id`
    - `delivery_id` eq `path.delivery_id`
  - Notes:
    - Response body references #/components/schemas/hook-delivery
