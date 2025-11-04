# Component Plan: `payment_intent`

**API Slug:** `stripe`
**Total Routes:** 10

## Supported Operations
- **`create`**: Create a new record for the component.
- **`read_one`**: Fetch a single record by identifier.
- **`read_many`**: List or search records.

## Routes

### GET Routes (2)

#### `GET /v1/payment_intents`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `payment_intent`
  - Notes:
    - Query parameters: created, customer, ending_before, expand, limit, starting_after

#### `GET /v1/payment_intents/{intent}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `payment_intent`
  - Filters:
    - `intent` eq `path.intent`
  - Notes:
    - Response body references #/components/schemas/payment_intent
    - Query parameters: client_secret, expand

### POST Routes (8)

#### `POST /v1/payment_intents`
**Status:** planned

**Operations:**
- **create**
  - Component: `payment_intent`
  - Notes:
    - Response body references #/components/schemas/payment_intent

#### `POST /v1/payment_intents/{intent}`
**Status:** planned

**Operations:**
- **create**
  - Component: `payment_intent`
  - Filters:
    - `intent` eq `path.intent`
  - Notes:
    - Response body references #/components/schemas/payment_intent
    - Query parameters: intent

#### `POST /v1/payment_intents/{intent}/apply_customer_balance`
**Status:** planned

**Operations:**
- **create**
  - Component: `payment_intent`
  - Filters:
    - `intent` eq `path.intent`
  - Notes:
    - Response body references #/components/schemas/payment_intent
    - Query parameters: intent

#### `POST /v1/payment_intents/{intent}/cancel`
**Status:** planned

**Operations:**
- **create**
  - Component: `payment_intent`
  - Filters:
    - `intent` eq `path.intent`
  - Notes:
    - Response body references #/components/schemas/payment_intent
    - Query parameters: intent

#### `POST /v1/payment_intents/{intent}/capture`
**Status:** planned

**Operations:**
- **create**
  - Component: `payment_intent`
  - Filters:
    - `intent` eq `path.intent`
  - Notes:
    - Response body references #/components/schemas/payment_intent
    - Query parameters: intent

#### `POST /v1/payment_intents/{intent}/confirm`
**Status:** planned

**Operations:**
- **create**
  - Component: `payment_intent`
  - Filters:
    - `intent` eq `path.intent`
  - Notes:
    - Response body references #/components/schemas/payment_intent
    - Query parameters: intent

#### `POST /v1/payment_intents/{intent}/increment_authorization`
**Status:** planned

**Operations:**
- **create**
  - Component: `payment_intent`
  - Filters:
    - `intent` eq `path.intent`
  - Notes:
    - Response body references #/components/schemas/payment_intent
    - Query parameters: intent

#### `POST /v1/payment_intents/{intent}/verify_microdeposits`
**Status:** planned

**Operations:**
- **create**
  - Component: `payment_intent`
  - Filters:
    - `intent` eq `path.intent`
  - Notes:
    - Response body references #/components/schemas/payment_intent
    - Query parameters: intent
