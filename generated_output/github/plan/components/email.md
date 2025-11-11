# Component Plan: `email`

**API Slug:** `github`
**Total Routes:** 3

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_many`**: List or search records.
- **`delete`**: Remove a record.

## Routes

### DELETE Routes (1)

#### `DELETE /user/emails`
**Summary:** Delete an email address for the authenticated user
**Status:** planned

**Operations:**
- **delete**
  - Component: `email`

### GET Routes (1)

#### `GET /user/emails`
**Summary:** List email addresses for the authenticated user
**Status:** planned

**Operations:**
- **read_many**
  - Component: `email`

### POST Routes (1)

#### `POST /user/emails`
**Summary:** Add an email address for the authenticated user
**Status:** planned

**Operations:**
- **create**
  - Component: `email`
