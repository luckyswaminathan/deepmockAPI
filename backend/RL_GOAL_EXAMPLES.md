# RL Goal Examples for Stripe API

## Example 1: Create a Customer with Payment Method

**Goal**: Create a customer and attach a payment method to them.

```json
{
  "api_slug": "stripe",
  "description": "Create a customer with an active payment method",
  "goal_state": {
    "target_components": {
      "customer": [
        {
          "id": "cus_*",
          "email": "customer@example.com",
          "name": "John Doe"
        }
      ],
      "payment_method": [
        {
          "id": "pm_*",
          "customer": "cus_*",
          "type": "card",
          "card": {
            "brand": "visa",
            "last4": "4242"
          }
        }
      ]
    }
  }
}
```

## Example 2: Create a Successful Charge

**Goal**: Create a customer and process a successful charge.

```json
{
  "api_slug": "stripe",
  "description": "Create a customer and process a $100 charge",
  "goal_state": {
    "target_components": {
      "customer": [
        {
          "id": "cus_*",
          "email": "buyer@example.com"
        }
      ],
      "charge": [
        {
          "id": "ch_*",
          "customer": "cus_*",
          "amount": 10000,
          "currency": "usd",
          "status": "succeeded",
          "paid": true
        }
      ]
    }
  }
}
```

## Example 3: Create Account with Capability

**Goal**: Create a Stripe Connect account and enable a capability.

```json
{
  "api_slug": "stripe",
  "description": "Create a Connect account with transfers capability enabled",
  "goal_state": {
    "target_components": {
      "account": [
        {
          "id": "acct_*",
          "type": "express",
          "country": "US"
        }
      ],
      "capability": [
        {
          "id": "acct_*",
          "capability": "transfers",
          "status": "active",
          "requirements": {
            "currently_due": [],
            "eventually_due": []
          }
        }
      ]
    }
  }
}
```

## Example 4: Update Customer Status

**Goal**: Change a customer's account status to active.

```json
{
  "api_slug": "stripe",
  "description": "Update customer account status to active",
  "goal_state": {
    "target_components": {
      "customer": [
        {
          "id": "cus_existing123",
          "email": "customer@example.com",
          "status": "active",
          "delinquent": false
        }
      ]
    }
  }
}
```

## Example 5: Create Subscription

**Goal**: Create a customer with an active subscription.

```json
{
  "api_slug": "stripe",
  "description": "Create customer with active subscription",
  "goal_state": {
    "target_components": {
      "customer": [
        {
          "id": "cus_*",
          "email": "subscriber@example.com"
        }
      ],
      "subscription": [
        {
          "id": "sub_*",
          "customer": "cus_*",
          "status": "active",
          "current_period_end": 1735689600,
          "items": {
            "data": [
              {
                "price": {
                  "id": "price_*",
                  "product": "prod_*"
                }
              }
            ]
          }
        }
      ]
    }
  }
}
```

## Notes

- Use `*` as a wildcard for IDs that will be generated
- The `goal_state.target_components` structure matches the `modified_components` format used in states
- Each component name corresponds to a Stripe API resource
- The RL system will match states based on these target components
- Partial matches are supported (you don't need to specify every field, just the ones that matter for the goal)

