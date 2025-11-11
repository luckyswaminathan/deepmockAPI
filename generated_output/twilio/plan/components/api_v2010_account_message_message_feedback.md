# Component Plan: `api.v2010.account.message.message_feedback`

**API Slug:** `twilio`
**Total Routes:** 1

## Supported Operations
- **`create`**: Create a new record for the component.

## Routes

### POST Routes (1)

#### `POST /2010-04-01/Accounts/{AccountSid}/Messages/{MessageSid}/Feedback.json`
**Summary:** Create Message Feedback to confirm a tracked user action was performed by the recipient of the associated Message
**Status:** planned

**Operations:**
- **create**
  - Component: `api.v2010.account.message.message_feedback`
  - Filters:
    - `AccountSid` eq `path.AccountSid`
    - `MessageSid` eq `path.MessageSid`
  - Notes:
    - Response body references #/components/schemas/api.v2010.account.message.message_feedback
    - Query parameters: AccountSid, MessageSid
