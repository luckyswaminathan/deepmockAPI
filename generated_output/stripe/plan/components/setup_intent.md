# Component Plan: `setup_intent`

**API Slug:** `stripe`
**Total Routes:** 7

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.

## Routes

### GET Routes (2)

#### `GET /v1/setup_intents`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `setup_intent`
  - Notes:
    - Query parameters: attach_to_self, created, customer, ending_before, expand, limit, payment_method, starting_after

#### `GET /v1/setup_intents/{intent}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `setup_intent`
  - Filters:
    - `intent` eq `path.intent`
  - Notes:
    - Response body references #/components/schemas/setup_intent
    - Query parameters: client_secret, expand

### POST Routes (5)

#### `POST /v1/setup_intents`
**Status:** planned

**Operations:**
- **create**
  - Component: `setup_intent`
  - Notes:
    - Response body references #/components/schemas/setup_intent

#### `POST /v1/setup_intents/{intent}`
**Status:** planned

**Operations:**
- **create**
  - Component: `setup_intent`
  - Filters:
    - `intent` eq `path.intent`
  - Notes:
    - Response body references #/components/schemas/setup_intent
    - Query parameters: intent

#### `POST /v1/setup_intents/{intent}/cancel`
**Status:** planned

**Operations:**
- **create**
  - Component: `setup_intent`
  - Filters:
    - `intent` eq `path.intent`
  - Notes:
    - Response body references #/components/schemas/setup_intent
    - Query parameters: intent

#### `POST /v1/setup_intents/{intent}/confirm`
**Status:** planned

**Operations:**
- **create**
  - Component: `setup_intent`
  - Filters:
    - `intent` eq `path.intent`
  - Notes:
    - Response body references #/components/schemas/setup_intent
    - Query parameters: intent

#### `POST /v1/setup_intents/{intent}/verify_microdeposits`
**Status:** planned

**Operations:**
- **create**
  - Component: `setup_intent`
  - Filters:
    - `intent` eq `path.intent`
  - Notes:
    - Response body references #/components/schemas/setup_intent
    - Query parameters: intent
