# Generated API Routes for `stripe`

**Generated at:** 2025-11-01T20:16:47.085860+00:00

This document describes all generated API routes and their operations.

## Routes by Component

### Component: `account`

#### `GET /v1/account`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `account`
  - Notes:
    - Response body references #/components/schemas/account
    - Query parameters: expand

#### `GET /v1/accounts/{account}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `account`
  - Filters:
    - `external_accounts` eq `path.account`
  - Notes:
    - Response body references #/components/schemas/account
    - Query parameters: expand

#### `POST /v1/accounts`
**Status:** planned

**Operations:**
- **create**
  - Component: `account`
  - Notes:
    - Response body references #/components/schemas/account

#### `POST /v1/accounts/{account}`
**Status:** planned

**Operations:**
- **create**
  - Component: `account`
  - Filters:
    - `external_accounts` eq `path.account`
  - Notes:
    - Response body references #/components/schemas/account
    - Query parameters: account

#### `POST /v1/accounts/{account}/reject`
**Status:** planned

**Operations:**
- **create**
  - Component: `account`
  - Filters:
    - `external_accounts` eq `path.account`
  - Notes:
    - Response body references #/components/schemas/account
    - Query parameters: account

### Component: `account_link`

#### `POST /v1/account_links`
**Status:** planned

**Operations:**
- **create**
  - Component: `account_link`
  - Notes:
    - Response body references #/components/schemas/account_link

### Component: `account_session`

#### `POST /v1/account_sessions`
**Status:** planned

**Operations:**
- **create**
  - Component: `account_session`
  - Notes:
    - Response body references #/components/schemas/account_session

### Component: `apple_pay_domain`

#### `GET /v1/apple_pay/domains/{domain}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `apple_pay_domain`
  - Filters:
    - `domain_name` eq `path.domain`
  - Notes:
    - Response body references #/components/schemas/apple_pay_domain
    - Query parameters: expand

#### `POST /v1/apple_pay/domains`
**Status:** planned

**Operations:**
- **create**
  - Component: `apple_pay_domain`
  - Notes:
    - Response body references #/components/schemas/apple_pay_domain

### Component: `application_fee`

#### `GET /v1/application_fees/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `application_fee`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/application_fee
    - Query parameters: expand

#### `POST /v1/application_fees/{id}/refund`
**Status:** planned

**Operations:**
- **create**
  - Component: `application_fee`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/application_fee
    - Query parameters: id

### Component: `apps.secret`

#### `GET /v1/apps/secrets/find`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `apps.secret`
  - Notes:
    - Response body references #/components/schemas/apps.secret
    - Query parameters: expand, name, scope

#### `POST /v1/apps/secrets`
**Status:** planned

**Operations:**
- **create**
  - Component: `apps.secret`
  - Notes:
    - Response body references #/components/schemas/apps.secret

#### `POST /v1/apps/secrets/delete`
**Status:** planned

**Operations:**
- **create**
  - Component: `apps.secret`
  - Notes:
    - Response body references #/components/schemas/apps.secret

### Component: `balance`

#### `GET /v1/balance`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `balance`
  - Notes:
    - Response body references #/components/schemas/balance
    - Query parameters: expand

### Component: `balance_transaction`

#### `GET /v1/balance/history/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `balance_transaction`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/balance_transaction
    - Query parameters: expand

#### `GET /v1/balance_transactions/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `balance_transaction`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/balance_transaction
    - Query parameters: expand

### Component: `bank_account`

#### `GET /v1/customers/{customer}/bank_accounts/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `bank_account`
  - Filters:
    - `customer` eq `path.customer`
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/bank_account
    - Query parameters: expand

#### `POST /v1/customers/{customer}/bank_accounts/{id}/verify`
**Status:** planned

**Operations:**
- **create**
  - Component: `bank_account`
  - Filters:
    - `customer` eq `path.customer`
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/bank_account
    - Query parameters: customer, id

#### `POST /v1/customers/{customer}/sources/{id}/verify`
**Status:** planned

**Operations:**
- **create**
  - Component: `bank_account`
  - Filters:
    - `customer` eq `path.customer`
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/bank_account
    - Query parameters: customer, id

### Component: `billing.alert`

#### `GET /v1/billing/alerts/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `billing.alert`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/billing.alert
    - Query parameters: expand

#### `POST /v1/billing/alerts`
**Status:** planned

**Operations:**
- **create**
  - Component: `billing.alert`
  - Notes:
    - Response body references #/components/schemas/billing.alert

#### `POST /v1/billing/alerts/{id}/activate`
**Status:** planned

**Operations:**
- **create**
  - Component: `billing.alert`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/billing.alert
    - Query parameters: id

#### `POST /v1/billing/alerts/{id}/archive`
**Status:** planned

**Operations:**
- **create**
  - Component: `billing.alert`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/billing.alert
    - Query parameters: id

#### `POST /v1/billing/alerts/{id}/deactivate`
**Status:** planned

**Operations:**
- **create**
  - Component: `billing.alert`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/billing.alert
    - Query parameters: id

### Component: `billing.credit_balance_summary`

#### `GET /v1/billing/credit_balance_summary`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `billing.credit_balance_summary`
  - Notes:
    - Response body references #/components/schemas/billing.credit_balance_summary
    - Query parameters: customer, expand, filter

### Component: `billing.credit_balance_transaction`

#### `GET /v1/billing/credit_balance_transactions/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `billing.credit_balance_transaction`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/billing.credit_balance_transaction
    - Query parameters: expand

### Component: `billing.credit_grant`

#### `GET /v1/billing/credit_grants/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `billing.credit_grant`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/billing.credit_grant
    - Query parameters: expand

#### `POST /v1/billing/credit_grants`
**Status:** planned

**Operations:**
- **create**
  - Component: `billing.credit_grant`
  - Notes:
    - Response body references #/components/schemas/billing.credit_grant

#### `POST /v1/billing/credit_grants/{id}`
**Status:** planned

**Operations:**
- **create**
  - Component: `billing.credit_grant`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/billing.credit_grant
    - Query parameters: id

#### `POST /v1/billing/credit_grants/{id}/expire`
**Status:** planned

**Operations:**
- **create**
  - Component: `billing.credit_grant`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/billing.credit_grant
    - Query parameters: id

#### `POST /v1/billing/credit_grants/{id}/void`
**Status:** planned

**Operations:**
- **create**
  - Component: `billing.credit_grant`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/billing.credit_grant
    - Query parameters: id

### Component: `billing.meter`

#### `GET /v1/billing/meters/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `billing.meter`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/billing.meter
    - Query parameters: expand

#### `POST /v1/billing/meters`
**Status:** planned

**Operations:**
- **create**
  - Component: `billing.meter`
  - Notes:
    - Response body references #/components/schemas/billing.meter

#### `POST /v1/billing/meters/{id}`
**Status:** planned

**Operations:**
- **create**
  - Component: `billing.meter`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/billing.meter
    - Query parameters: id

#### `POST /v1/billing/meters/{id}/deactivate`
**Status:** planned

**Operations:**
- **create**
  - Component: `billing.meter`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/billing.meter
    - Query parameters: id

#### `POST /v1/billing/meters/{id}/reactivate`
**Status:** planned

**Operations:**
- **create**
  - Component: `billing.meter`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/billing.meter
    - Query parameters: id

### Component: `billing.meter_event`

#### `POST /v1/billing/meter_events`
**Status:** planned

**Operations:**
- **create**
  - Component: `billing.meter_event`
  - Notes:
    - Response body references #/components/schemas/billing.meter_event

### Component: `billing.meter_event_adjustment`

#### `POST /v1/billing/meter_event_adjustments`
**Status:** planned

**Operations:**
- **create**
  - Component: `billing.meter_event_adjustment`
  - Notes:
    - Response body references #/components/schemas/billing.meter_event_adjustment

### Component: `billing_portal.configuration`

#### `GET /v1/billing_portal/configurations/{configuration}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `billing_portal.configuration`
  - Filters:
    - `configuration` eq `path.configuration`
  - Notes:
    - Response body references #/components/schemas/billing_portal.configuration
    - Query parameters: expand

#### `POST /v1/billing_portal/configurations`
**Status:** planned

**Operations:**
- **create**
  - Component: `billing_portal.configuration`
  - Notes:
    - Response body references #/components/schemas/billing_portal.configuration

#### `POST /v1/billing_portal/configurations/{configuration}`
**Status:** planned

**Operations:**
- **create**
  - Component: `billing_portal.configuration`
  - Filters:
    - `configuration` eq `path.configuration`
  - Notes:
    - Response body references #/components/schemas/billing_portal.configuration
    - Query parameters: configuration

### Component: `billing_portal.session`

#### `POST /v1/billing_portal/sessions`
**Status:** planned

**Operations:**
- **create**
  - Component: `billing_portal.session`
  - Notes:
    - Response body references #/components/schemas/billing_portal.session

### Component: `capability`

#### `GET /v1/accounts/{account}/capabilities/{capability}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `capability`
  - Filters:
    - `account` eq `path.account`
    - `capability` eq `path.capability`
  - Notes:
    - Response body references #/components/schemas/capability
    - Query parameters: expand

#### `POST /v1/accounts/{account}/capabilities/{capability}`
**Status:** planned

**Operations:**
- **create**
  - Component: `capability`
  - Filters:
    - `account` eq `path.account`
    - `capability` eq `path.capability`
  - Notes:
    - Response body references #/components/schemas/capability
    - Query parameters: account, capability

### Component: `card`

#### `GET /v1/customers/{customer}/cards/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `card`
  - Filters:
    - `customer` eq `path.customer`
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/card
    - Query parameters: expand

### Component: `cash_balance`

#### `GET /v1/customers/{customer}/cash_balance`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `cash_balance`
  - Filters:
    - `customer` eq `path.customer`
  - Notes:
    - Response body references #/components/schemas/cash_balance
    - Query parameters: expand

#### `POST /v1/customers/{customer}/cash_balance`
**Status:** planned

**Operations:**
- **create**
  - Component: `cash_balance`
  - Filters:
    - `customer` eq `path.customer`
  - Notes:
    - Response body references #/components/schemas/cash_balance
    - Query parameters: customer

### Component: `charge`

#### `GET /v1/charges/{charge}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `charge`
  - Filters:
    - `charge` eq `path.charge`
  - Notes:
    - Response body references #/components/schemas/charge
    - Query parameters: expand

#### `POST /v1/charges`
**Status:** planned

**Operations:**
- **create**
  - Component: `charge`
  - Notes:
    - Response body references #/components/schemas/charge

#### `POST /v1/charges/{charge}`
**Status:** planned

**Operations:**
- **create**
  - Component: `charge`
  - Filters:
    - `charge` eq `path.charge`
  - Notes:
    - Response body references #/components/schemas/charge
    - Query parameters: charge

#### `POST /v1/charges/{charge}/capture`
**Status:** planned

**Operations:**
- **create**
  - Component: `charge`
  - Filters:
    - `charge` eq `path.charge`
  - Notes:
    - Response body references #/components/schemas/charge
    - Query parameters: charge

#### `POST /v1/charges/{charge}/refund`
**Status:** planned

**Operations:**
- **create**
  - Component: `charge`
  - Filters:
    - `charge` eq `path.charge`
  - Notes:
    - Response body references #/components/schemas/charge
    - Query parameters: charge

### Component: `checkout.session`

#### `GET /v1/checkout/sessions/{session}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `checkout.session`
  - Filters:
    - `session` eq `path.session`
  - Notes:
    - Response body references #/components/schemas/checkout.session
    - Query parameters: expand

#### `POST /v1/checkout/sessions`
**Status:** planned

**Operations:**
- **create**
  - Component: `checkout.session`
  - Notes:
    - Response body references #/components/schemas/checkout.session

#### `POST /v1/checkout/sessions/{session}`
**Status:** planned

**Operations:**
- **create**
  - Component: `checkout.session`
  - Filters:
    - `session` eq `path.session`
  - Notes:
    - Response body references #/components/schemas/checkout.session
    - Query parameters: session

#### `POST /v1/checkout/sessions/{session}/expire`
**Status:** planned

**Operations:**
- **create**
  - Component: `checkout.session`
  - Filters:
    - `session` eq `path.session`
  - Notes:
    - Response body references #/components/schemas/checkout.session
    - Query parameters: session

### Component: `climate.order`

#### `GET /v1/climate/orders/{order}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `climate.order`
  - Filters:
    - `order` eq `path.order`
  - Notes:
    - Response body references #/components/schemas/climate.order
    - Query parameters: expand

#### `POST /v1/climate/orders`
**Status:** planned

**Operations:**
- **create**
  - Component: `climate.order`
  - Notes:
    - Response body references #/components/schemas/climate.order

#### `POST /v1/climate/orders/{order}`
**Status:** planned

**Operations:**
- **create**
  - Component: `climate.order`
  - Filters:
    - `order` eq `path.order`
  - Notes:
    - Response body references #/components/schemas/climate.order
    - Query parameters: order

#### `POST /v1/climate/orders/{order}/cancel`
**Status:** planned

**Operations:**
- **create**
  - Component: `climate.order`
  - Filters:
    - `order` eq `path.order`
  - Notes:
    - Response body references #/components/schemas/climate.order
    - Query parameters: order

### Component: `climate.product`

#### `GET /v1/climate/products/{product}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `climate.product`
  - Filters:
    - `product` eq `path.product`
  - Notes:
    - Response body references #/components/schemas/climate.product
    - Query parameters: expand

### Component: `climate.supplier`

#### `GET /v1/climate/suppliers/{supplier}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `climate.supplier`
  - Filters:
    - `supplier` eq `path.supplier`
  - Notes:
    - Response body references #/components/schemas/climate.supplier
    - Query parameters: expand

### Component: `confirmation_token`

#### `GET /v1/confirmation_tokens/{confirmation_token}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `confirmation_token`
  - Filters:
    - `confirmation_token` eq `path.confirmation_token`
  - Notes:
    - Response body references #/components/schemas/confirmation_token
    - Query parameters: expand

#### `POST /v1/test_helpers/confirmation_tokens`
**Status:** planned

**Operations:**
- **create**
  - Component: `confirmation_token`
  - Notes:
    - Response body references #/components/schemas/confirmation_token

### Component: `country_spec`

#### `GET /v1/country_specs/{country}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `country_spec`
  - Filters:
    - `country` eq `path.country`
  - Notes:
    - Response body references #/components/schemas/country_spec
    - Query parameters: expand

### Component: `coupon`

#### `GET /v1/coupons/{coupon}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `coupon`
  - Filters:
    - `coupon` eq `path.coupon`
  - Notes:
    - Response body references #/components/schemas/coupon
    - Query parameters: expand

#### `POST /v1/coupons`
**Status:** planned

**Operations:**
- **create**
  - Component: `coupon`
  - Notes:
    - Response body references #/components/schemas/coupon

#### `POST /v1/coupons/{coupon}`
**Status:** planned

**Operations:**
- **create**
  - Component: `coupon`
  - Filters:
    - `coupon` eq `path.coupon`
  - Notes:
    - Response body references #/components/schemas/coupon
    - Query parameters: coupon

### Component: `credit_note`

#### `GET /v1/credit_notes/preview`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `credit_note`
  - Notes:
    - Response body references #/components/schemas/credit_note
    - Query parameters: amount, credit_amount, effective_at, email_type, expand, invoice, lines, memo, metadata, out_of_band_amount, reason, refund, refund_amount, shipping_cost

#### `GET /v1/credit_notes/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `credit_note`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/credit_note
    - Query parameters: expand

#### `POST /v1/credit_notes`
**Status:** planned

**Operations:**
- **create**
  - Component: `credit_note`
  - Notes:
    - Response body references #/components/schemas/credit_note

#### `POST /v1/credit_notes/{id}`
**Status:** planned

**Operations:**
- **create**
  - Component: `credit_note`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/credit_note
    - Query parameters: id

#### `POST /v1/credit_notes/{id}/void`
**Status:** planned

**Operations:**
- **create**
  - Component: `credit_note`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/credit_note
    - Query parameters: id

### Component: `customer`

#### `POST /v1/customers`
**Status:** planned

**Operations:**
- **create**
  - Component: `customer`
  - Notes:
    - Response body references #/components/schemas/customer

#### `POST /v1/customers/{customer}`
**Status:** planned

**Operations:**
- **create**
  - Component: `customer`
  - Filters:
    - `customer` eq `path.customer`
  - Notes:
    - Response body references #/components/schemas/customer
    - Query parameters: customer

### Component: `customer_balance_transaction`

#### `GET /v1/customers/{customer}/balance_transactions/{transaction}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `customer_balance_transaction`
  - Filters:
    - `customer` eq `path.customer`
    - `transaction` eq `path.transaction`
  - Notes:
    - Response body references #/components/schemas/customer_balance_transaction
    - Query parameters: expand

#### `POST /v1/customers/{customer}/balance_transactions`
**Status:** planned

**Operations:**
- **create**
  - Component: `customer_balance_transaction`
  - Filters:
    - `customer` eq `path.customer`
  - Notes:
    - Response body references #/components/schemas/customer_balance_transaction
    - Query parameters: customer

#### `POST /v1/customers/{customer}/balance_transactions/{transaction}`
**Status:** planned

**Operations:**
- **create**
  - Component: `customer_balance_transaction`
  - Filters:
    - `customer` eq `path.customer`
    - `transaction` eq `path.transaction`
  - Notes:
    - Response body references #/components/schemas/customer_balance_transaction
    - Query parameters: customer, transaction

### Component: `customer_cash_balance_transaction`

#### `GET /v1/customers/{customer}/cash_balance_transactions/{transaction}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `customer_cash_balance_transaction`
  - Filters:
    - `customer` eq `path.customer`
    - `transaction` eq `path.transaction`
  - Notes:
    - Response body references #/components/schemas/customer_cash_balance_transaction
    - Query parameters: expand

#### `POST /v1/test_helpers/customers/{customer}/fund_cash_balance`
**Status:** planned

**Operations:**
- **create**
  - Component: `customer_cash_balance_transaction`
  - Filters:
    - `customer` eq `path.customer`
  - Notes:
    - Response body references #/components/schemas/customer_cash_balance_transaction
    - Query parameters: customer

### Component: `customer_session`

#### `POST /v1/customer_sessions`
**Status:** planned

**Operations:**
- **create**
  - Component: `customer_session`
  - Notes:
    - Response body references #/components/schemas/customer_session

### Component: `deleted_account`

#### `DELETE /v1/accounts/{account}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `deleted_account`
  - Filters:
    - `account` eq `path.account`
  - Notes:
    - Response body references #/components/schemas/deleted_account
    - Query parameters: account

### Component: `deleted_apple_pay_domain`

#### `DELETE /v1/apple_pay/domains/{domain}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `deleted_apple_pay_domain`
  - Filters:
    - `domain` eq `path.domain`
  - Notes:
    - Response body references #/components/schemas/deleted_apple_pay_domain
    - Query parameters: domain

### Component: `deleted_coupon`

#### `DELETE /v1/coupons/{coupon}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `deleted_coupon`
  - Filters:
    - `coupon` eq `path.coupon`
  - Notes:
    - Response body references #/components/schemas/deleted_coupon
    - Query parameters: coupon

### Component: `deleted_customer`

#### `DELETE /v1/customers/{customer}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `deleted_customer`
  - Filters:
    - `customer` eq `path.customer`
  - Notes:
    - Response body references #/components/schemas/deleted_customer
    - Query parameters: customer

### Component: `deleted_discount`

#### `DELETE /v1/customers/{customer}/discount`
**Status:** planned

**Operations:**
- **delete**
  - Component: `deleted_discount`
  - Filters:
    - `customer` eq `path.customer`
  - Notes:
    - Response body references #/components/schemas/deleted_discount
    - Query parameters: customer

#### `DELETE /v1/customers/{customer}/subscriptions/{subscription_exposed_id}/discount`
**Status:** planned

**Operations:**
- **delete**
  - Component: `deleted_discount`
  - Filters:
    - `customer` eq `path.customer`
    - `subscription_exposed_id` eq `path.subscription_exposed_id`
  - Notes:
    - Response body references #/components/schemas/deleted_discount
    - Query parameters: customer, subscription_exposed_id

#### `DELETE /v1/subscriptions/{subscription_exposed_id}/discount`
**Status:** planned

**Operations:**
- **delete**
  - Component: `deleted_discount`
  - Filters:
    - `subscription_exposed_id` eq `path.subscription_exposed_id`
  - Notes:
    - Response body references #/components/schemas/deleted_discount
    - Query parameters: subscription_exposed_id

### Component: `deleted_external_account`

#### `DELETE /v1/accounts/{account}/bank_accounts/{id}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `deleted_external_account`
  - Filters:
    - `account` eq `path.account`
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/deleted_external_account
    - Query parameters: account, id

#### `DELETE /v1/accounts/{account}/external_accounts/{id}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `deleted_external_account`
  - Filters:
    - `account` eq `path.account`
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/deleted_external_account
    - Query parameters: account, id

### Component: `deleted_invoice`

#### `DELETE /v1/invoices/{invoice}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `deleted_invoice`
  - Filters:
    - `invoice` eq `path.invoice`
  - Notes:
    - Response body references #/components/schemas/deleted_invoice
    - Query parameters: invoice

### Component: `deleted_invoiceitem`

#### `DELETE /v1/invoiceitems/{invoiceitem}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `deleted_invoiceitem`
  - Filters:
    - `invoiceitem` eq `path.invoiceitem`
  - Notes:
    - Response body references #/components/schemas/deleted_invoiceitem
    - Query parameters: invoiceitem

### Component: `deleted_person`

#### `DELETE /v1/accounts/{account}/people/{person}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `deleted_person`
  - Filters:
    - `account` eq `path.account`
    - `person` eq `path.person`
  - Notes:
    - Response body references #/components/schemas/deleted_person
    - Query parameters: account, person

#### `DELETE /v1/accounts/{account}/persons/{person}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `deleted_person`
  - Filters:
    - `account` eq `path.account`
    - `person` eq `path.person`
  - Notes:
    - Response body references #/components/schemas/deleted_person
    - Query parameters: account, person

### Component: `deleted_plan`

#### `DELETE /v1/plans/{plan}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `deleted_plan`
  - Filters:
    - `plan` eq `path.plan`
  - Notes:
    - Response body references #/components/schemas/deleted_plan
    - Query parameters: plan

### Component: `deleted_product`

#### `DELETE /v1/products/{id}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `deleted_product`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/deleted_product
    - Query parameters: id

### Component: `deleted_product_feature`

#### `DELETE /v1/products/{product}/features/{id}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `deleted_product_feature`
  - Filters:
    - `id` eq `path.id`
    - `product` eq `path.product`
  - Notes:
    - Response body references #/components/schemas/deleted_product_feature
    - Query parameters: id, product

### Component: `deleted_radar.value_list`

#### `DELETE /v1/radar/value_lists/{value_list}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `deleted_radar.value_list`
  - Filters:
    - `value_list` eq `path.value_list`
  - Notes:
    - Response body references #/components/schemas/deleted_radar.value_list
    - Query parameters: value_list

### Component: `deleted_radar.value_list_item`

#### `DELETE /v1/radar/value_list_items/{item}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `deleted_radar.value_list_item`
  - Filters:
    - `item` eq `path.item`
  - Notes:
    - Response body references #/components/schemas/deleted_radar.value_list_item
    - Query parameters: item

### Component: `deleted_subscription_item`

#### `DELETE /v1/subscription_items/{item}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `deleted_subscription_item`
  - Filters:
    - `item` eq `path.item`
  - Notes:
    - Response body references #/components/schemas/deleted_subscription_item
    - Query parameters: item

### Component: `deleted_tax_id`

#### `DELETE /v1/customers/{customer}/tax_ids/{id}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `deleted_tax_id`
  - Filters:
    - `customer` eq `path.customer`
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/deleted_tax_id
    - Query parameters: customer, id

#### `DELETE /v1/tax_ids/{id}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `deleted_tax_id`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/deleted_tax_id
    - Query parameters: id

### Component: `deleted_terminal.configuration`

#### `DELETE /v1/terminal/configurations/{configuration}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `deleted_terminal.configuration`
  - Filters:
    - `configuration` eq `path.configuration`
  - Notes:
    - Response body references #/components/schemas/deleted_terminal.configuration
    - Query parameters: configuration

### Component: `deleted_terminal.location`

#### `DELETE /v1/terminal/locations/{location}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `deleted_terminal.location`
  - Filters:
    - `location` eq `path.location`
  - Notes:
    - Response body references #/components/schemas/deleted_terminal.location
    - Query parameters: location

### Component: `deleted_terminal.reader`

#### `DELETE /v1/terminal/readers/{reader}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `deleted_terminal.reader`
  - Filters:
    - `reader` eq `path.reader`
  - Notes:
    - Response body references #/components/schemas/deleted_terminal.reader
    - Query parameters: reader

### Component: `deleted_test_helpers.test_clock`

#### `DELETE /v1/test_helpers/test_clocks/{test_clock}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `deleted_test_helpers.test_clock`
  - Filters:
    - `test_clock` eq `path.test_clock`
  - Notes:
    - Response body references #/components/schemas/deleted_test_helpers.test_clock
    - Query parameters: test_clock

### Component: `deleted_webhook_endpoint`

#### `DELETE /v1/webhook_endpoints/{webhook_endpoint}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `deleted_webhook_endpoint`
  - Filters:
    - `webhook_endpoint` eq `path.webhook_endpoint`
  - Notes:
    - Response body references #/components/schemas/deleted_webhook_endpoint
    - Query parameters: webhook_endpoint

### Component: `discount`

#### `GET /v1/customers/{customer}/discount`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `discount`
  - Filters:
    - `customer` eq `path.customer`
  - Notes:
    - Response body references #/components/schemas/discount
    - Query parameters: expand

#### `GET /v1/customers/{customer}/subscriptions/{subscription_exposed_id}/discount`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `discount`
  - Filters:
    - `customer` eq `path.customer`
    - `subscription_exposed_id` eq `path.subscription_exposed_id`
  - Notes:
    - Response body references #/components/schemas/discount
    - Query parameters: expand

### Component: `dispute`

#### `GET /v1/charges/{charge}/dispute`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `dispute`
  - Filters:
    - `charge` eq `path.charge`
  - Notes:
    - Response body references #/components/schemas/dispute
    - Query parameters: expand

#### `GET /v1/disputes/{dispute}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `dispute`
  - Filters:
    - `dispute` eq `path.dispute`
  - Notes:
    - Response body references #/components/schemas/dispute
    - Query parameters: expand

#### `POST /v1/charges/{charge}/dispute`
**Status:** planned

**Operations:**
- **create**
  - Component: `dispute`
  - Filters:
    - `charge` eq `path.charge`
  - Notes:
    - Response body references #/components/schemas/dispute
    - Query parameters: charge

#### `POST /v1/charges/{charge}/dispute/close`
**Status:** planned

**Operations:**
- **create**
  - Component: `dispute`
  - Filters:
    - `charge` eq `path.charge`
  - Notes:
    - Response body references #/components/schemas/dispute
    - Query parameters: charge

#### `POST /v1/disputes/{dispute}`
**Status:** planned

**Operations:**
- **create**
  - Component: `dispute`
  - Filters:
    - `dispute` eq `path.dispute`
  - Notes:
    - Response body references #/components/schemas/dispute
    - Query parameters: dispute

#### `POST /v1/disputes/{dispute}/close`
**Status:** planned

**Operations:**
- **create**
  - Component: `dispute`
  - Filters:
    - `dispute` eq `path.dispute`
  - Notes:
    - Response body references #/components/schemas/dispute
    - Query parameters: dispute

### Component: `entitlements.active_entitlement`

#### `GET /v1/entitlements/active_entitlements/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `entitlements.active_entitlement`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/entitlements.active_entitlement
    - Query parameters: expand

### Component: `entitlements.feature`

#### `GET /v1/entitlements/features/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `entitlements.feature`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/entitlements.feature
    - Query parameters: expand

#### `POST /v1/entitlements/features`
**Status:** planned

**Operations:**
- **create**
  - Component: `entitlements.feature`
  - Notes:
    - Response body references #/components/schemas/entitlements.feature

#### `POST /v1/entitlements/features/{id}`
**Status:** planned

**Operations:**
- **create**
  - Component: `entitlements.feature`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/entitlements.feature
    - Query parameters: id

### Component: `ephemeral_key`

#### `DELETE /v1/ephemeral_keys/{key}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `ephemeral_key`
  - Filters:
    - `key` eq `path.key`
  - Notes:
    - Response body references #/components/schemas/ephemeral_key
    - Query parameters: key

#### `POST /v1/ephemeral_keys`
**Status:** planned

**Operations:**
- **create**
  - Component: `ephemeral_key`
  - Notes:
    - Response body references #/components/schemas/ephemeral_key

### Component: `error`

#### `DELETE /v1/customers/{customer}/bank_accounts/{id}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `error`
  - Filters:
    - `customer` eq `path.customer`
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: customer, id

#### `DELETE /v1/customers/{customer}/cards/{id}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `error`
  - Filters:
    - `customer` eq `path.customer`
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: customer, id

#### `DELETE /v1/customers/{customer}/sources/{id}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `error`
  - Filters:
    - `customer` eq `path.customer`
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: customer, id

#### `GET /v1/accounts`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: created, ending_before, expand, limit, starting_after

#### `GET /v1/accounts/{account}/capabilities`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `error`
  - Filters:
    - `account` eq `path.account`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: expand

#### `GET /v1/accounts/{account}/external_accounts`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `error`
  - Filters:
    - `account` eq `path.account`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, limit, object, starting_after

#### `GET /v1/accounts/{account}/people`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `error`
  - Filters:
    - `account` eq `path.account`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, limit, relationship, starting_after

#### `GET /v1/accounts/{account}/persons`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `error`
  - Filters:
    - `account` eq `path.account`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, limit, relationship, starting_after

#### `GET /v1/apple_pay/domains`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: domain_name, ending_before, expand, limit, starting_after

#### `GET /v1/application_fees`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: charge, created, ending_before, expand, limit, starting_after

#### `GET /v1/application_fees/{id}/refunds`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `error`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, limit, starting_after

#### `GET /v1/apps/secrets`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, limit, scope, starting_after

#### `GET /v1/balance/history`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: created, currency, ending_before, expand, limit, payout, source, starting_after, type

#### `GET /v1/balance_transactions`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: created, currency, ending_before, expand, limit, payout, source, starting_after, type

#### `GET /v1/billing/alerts`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: alert_type, ending_before, expand, limit, meter, starting_after

#### `GET /v1/billing/credit_balance_transactions`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: credit_grant, customer, ending_before, expand, limit, starting_after

#### `GET /v1/billing/credit_grants`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: customer, ending_before, expand, limit, starting_after

#### `GET /v1/billing/meters`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, limit, starting_after, status

#### `GET /v1/billing/meters/{id}/event_summaries`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `error`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: customer, end_time, ending_before, expand, limit, start_time, starting_after, value_grouping_window

#### `GET /v1/billing_portal/configurations`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: active, ending_before, expand, is_default, limit, starting_after

#### `GET /v1/charges`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: created, customer, ending_before, expand, limit, payment_intent, starting_after, transfer_group

#### `GET /v1/charges/search`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: expand, limit, page, query

#### `GET /v1/charges/{charge}/refunds`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `error`
  - Filters:
    - `charge` eq `path.charge`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, limit, starting_after

#### `GET /v1/checkout/sessions`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: created, customer, customer_details, ending_before, expand, limit, payment_intent, payment_link, starting_after, status, subscription

#### `GET /v1/checkout/sessions/{session}/line_items`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `error`
  - Filters:
    - `session` eq `path.session`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, limit, starting_after

#### `GET /v1/climate/orders`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, limit, starting_after

#### `GET /v1/climate/products`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, limit, starting_after

#### `GET /v1/climate/suppliers`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, limit, starting_after

#### `GET /v1/country_specs`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, limit, starting_after

#### `GET /v1/coupons`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: created, ending_before, expand, limit, starting_after

#### `GET /v1/credit_notes`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: created, customer, ending_before, expand, invoice, limit, starting_after

#### `GET /v1/credit_notes/preview/lines`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: amount, credit_amount, effective_at, email_type, ending_before, expand, invoice, limit, lines, memo, metadata, out_of_band_amount, reason, refund, refund_amount, shipping_cost, starting_after

#### `GET /v1/credit_notes/{credit_note}/lines`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `error`
  - Filters:
    - `credit_note` eq `path.credit_note`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, limit, starting_after

#### `GET /v1/customers`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: created, email, ending_before, expand, limit, starting_after, test_clock

#### `GET /v1/customers/search`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: expand, limit, page, query

#### `GET /v1/customers/{customer}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `error`
  - Filters:
    - `customer` eq `path.customer`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: expand

#### `GET /v1/customers/{customer}/balance_transactions`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `error`
  - Filters:
    - `customer` eq `path.customer`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, limit, starting_after

#### `GET /v1/customers/{customer}/bank_accounts`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `error`
  - Filters:
    - `customer` eq `path.customer`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, limit, starting_after

#### `GET /v1/customers/{customer}/cards`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `error`
  - Filters:
    - `customer` eq `path.customer`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, limit, starting_after

#### `GET /v1/customers/{customer}/cash_balance_transactions`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `error`
  - Filters:
    - `customer` eq `path.customer`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, limit, starting_after

#### `GET /v1/customers/{customer}/payment_methods`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `error`
  - Filters:
    - `customer` eq `path.customer`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: allow_redisplay, ending_before, expand, limit, starting_after, type

#### `GET /v1/customers/{customer}/sources`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `error`
  - Filters:
    - `customer` eq `path.customer`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, limit, object, starting_after

#### `GET /v1/customers/{customer}/subscriptions`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `error`
  - Filters:
    - `customer` eq `path.customer`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, limit, starting_after

#### `GET /v1/customers/{customer}/tax_ids`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `error`
  - Filters:
    - `customer` eq `path.customer`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, limit, starting_after

#### `GET /v1/disputes`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: charge, created, ending_before, expand, limit, payment_intent, starting_after

#### `GET /v1/entitlements/active_entitlements`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: customer, ending_before, expand, limit, starting_after

#### `GET /v1/entitlements/features`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: archived, ending_before, expand, limit, lookup_key, starting_after

#### `GET /v1/events`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: created, delivery_success, ending_before, expand, limit, starting_after, type, types

#### `GET /v1/exchange_rates`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, limit, starting_after

#### `GET /v1/file_links`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: created, ending_before, expand, expired, file, limit, starting_after

#### `GET /v1/files`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: created, ending_before, expand, limit, purpose, starting_after

#### `GET /v1/financial_connections/accounts`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: account_holder, ending_before, expand, limit, session, starting_after

#### `GET /v1/financial_connections/accounts/{account}/owners`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `error`
  - Filters:
    - `account` eq `path.account`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, limit, ownership, starting_after

#### `GET /v1/financial_connections/transactions`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: account, ending_before, expand, limit, starting_after, transacted_at, transaction_refresh

#### `GET /v1/forwarding/requests`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: created, ending_before, expand, limit, starting_after

#### `GET /v1/identity/verification_reports`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: client_reference_id, created, ending_before, expand, limit, starting_after, type, verification_session

#### `GET /v1/identity/verification_sessions`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: client_reference_id, created, ending_before, expand, limit, related_customer, starting_after, status

#### `GET /v1/invoice_rendering_templates`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, limit, starting_after, status

#### `GET /v1/invoiceitems`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: created, customer, ending_before, expand, invoice, limit, pending, starting_after

#### `GET /v1/invoices`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: collection_method, created, customer, due_date, ending_before, expand, limit, starting_after, status, subscription

#### `GET /v1/invoices/search`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: expand, limit, page, query

#### `GET /v1/invoices/upcoming/lines`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: automatic_tax, coupon, currency, customer, customer_details, discounts, ending_before, expand, invoice_items, issuer, limit, on_behalf_of, preview_mode, schedule, schedule_details, starting_after, subscription, subscription_billing_cycle_anchor, subscription_cancel_at, subscription_cancel_at_period_end, subscription_cancel_now, subscription_default_tax_rates, subscription_details, subscription_items, subscription_proration_behavior, subscription_proration_date, subscription_resume_at, subscription_start_date, subscription_trial_end

#### `GET /v1/invoices/{invoice}/lines`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `error`
  - Filters:
    - `invoice` eq `path.invoice`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, limit, starting_after

#### `GET /v1/issuing/authorizations`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: card, cardholder, created, ending_before, expand, limit, starting_after, status

#### `GET /v1/issuing/cardholders`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: created, email, ending_before, expand, limit, phone_number, starting_after, status, type

#### `GET /v1/issuing/cards`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: cardholder, created, ending_before, exp_month, exp_year, expand, last4, limit, personalization_design, starting_after, status, type

#### `GET /v1/issuing/disputes`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: created, ending_before, expand, limit, starting_after, status, transaction

#### `GET /v1/issuing/personalization_designs`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, limit, lookup_keys, preferences, starting_after, status

#### `GET /v1/issuing/physical_bundles`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, limit, starting_after, status, type

#### `GET /v1/issuing/tokens`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: card, created, ending_before, expand, limit, starting_after, status

#### `GET /v1/issuing/transactions`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: card, cardholder, created, ending_before, expand, limit, starting_after, type

#### `GET /v1/linked_accounts`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: account_holder, ending_before, expand, limit, session, starting_after

#### `GET /v1/linked_accounts/{account}/owners`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `error`
  - Filters:
    - `account` eq `path.account`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, limit, ownership, starting_after

#### `GET /v1/payment_intents`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: created, customer, ending_before, expand, limit, starting_after

#### `GET /v1/payment_intents/search`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: expand, limit, page, query

#### `GET /v1/payment_links`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: active, ending_before, expand, limit, starting_after

#### `GET /v1/payment_links/{payment_link}/line_items`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `error`
  - Filters:
    - `payment_link` eq `path.payment_link`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, limit, starting_after

#### `GET /v1/payment_method_configurations`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: application, ending_before, expand, limit, starting_after

#### `GET /v1/payment_method_domains`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: domain_name, enabled, ending_before, expand, limit, starting_after

#### `GET /v1/payment_methods`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: customer, ending_before, expand, limit, starting_after, type

#### `GET /v1/payouts`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: arrival_date, created, destination, ending_before, expand, limit, starting_after, status

#### `GET /v1/plans`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: active, created, ending_before, expand, limit, product, starting_after

#### `GET /v1/prices`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: active, created, currency, ending_before, expand, limit, lookup_keys, product, recurring, starting_after, type

#### `GET /v1/prices/search`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: expand, limit, page, query

#### `GET /v1/products`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: active, created, ending_before, expand, ids, limit, shippable, starting_after, url

#### `GET /v1/products/search`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: expand, limit, page, query

#### `GET /v1/products/{product}/features`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `error`
  - Filters:
    - `product` eq `path.product`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, limit, starting_after

#### `GET /v1/promotion_codes`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: active, code, coupon, created, customer, ending_before, expand, limit, starting_after

#### `GET /v1/quotes`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: customer, ending_before, expand, limit, starting_after, status, test_clock

#### `GET /v1/quotes/{quote}/computed_upfront_line_items`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `error`
  - Filters:
    - `quote` eq `path.quote`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, limit, starting_after

#### `GET /v1/quotes/{quote}/line_items`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `error`
  - Filters:
    - `quote` eq `path.quote`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, limit, starting_after

#### `GET /v1/quotes/{quote}/pdf`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `error`
  - Filters:
    - `quote` eq `path.quote`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: expand

#### `GET /v1/radar/early_fraud_warnings`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: charge, created, ending_before, expand, limit, payment_intent, starting_after

#### `GET /v1/radar/value_list_items`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: created, ending_before, expand, limit, starting_after, value, value_list

#### `GET /v1/radar/value_lists`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: alias, contains, created, ending_before, expand, limit, starting_after

#### `GET /v1/refunds`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: charge, created, ending_before, expand, limit, payment_intent, starting_after

#### `GET /v1/reporting/report_runs`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: created, ending_before, expand, limit, starting_after

#### `GET /v1/reporting/report_types`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: expand

#### `GET /v1/reviews`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: created, ending_before, expand, limit, starting_after

#### `GET /v1/setup_attempts`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: created, ending_before, expand, limit, setup_intent, starting_after

#### `GET /v1/setup_intents`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: attach_to_self, created, customer, ending_before, expand, limit, payment_method, starting_after

#### `GET /v1/shipping_rates`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: active, created, currency, ending_before, expand, limit, starting_after

#### `GET /v1/sigma/scheduled_query_runs`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, limit, starting_after

#### `GET /v1/sources/{source}/source_transactions`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `error`
  - Filters:
    - `source` eq `path.source`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, limit, starting_after

#### `GET /v1/subscription_items`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, limit, starting_after, subscription

#### `GET /v1/subscription_items/{subscription_item}/usage_record_summaries`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `error`
  - Filters:
    - `subscription_item` eq `path.subscription_item`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, limit, starting_after

#### `GET /v1/subscription_schedules`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: canceled_at, completed_at, created, customer, ending_before, expand, limit, released_at, scheduled, starting_after

#### `GET /v1/subscriptions`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: automatic_tax, collection_method, created, current_period_end, current_period_start, customer, ending_before, expand, limit, price, starting_after, status, test_clock

#### `GET /v1/subscriptions/search`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: expand, limit, page, query

#### `GET /v1/tax/calculations/{calculation}/line_items`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `error`
  - Filters:
    - `calculation` eq `path.calculation`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, limit, starting_after

#### `GET /v1/tax/registrations`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, limit, starting_after, status

#### `GET /v1/tax/transactions/{transaction}/line_items`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `error`
  - Filters:
    - `transaction` eq `path.transaction`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, limit, starting_after

#### `GET /v1/tax_codes`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, limit, starting_after

#### `GET /v1/tax_ids`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, limit, owner, starting_after

#### `GET /v1/tax_rates`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: active, created, ending_before, expand, inclusive, limit, starting_after

#### `GET /v1/terminal/configurations`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, is_account_default, limit, starting_after

#### `GET /v1/terminal/configurations/{configuration}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `error`
  - Filters:
    - `configuration` eq `path.configuration`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: expand

#### `GET /v1/terminal/locations`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, limit, starting_after

#### `GET /v1/terminal/locations/{location}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `error`
  - Filters:
    - `location` eq `path.location`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: expand

#### `GET /v1/terminal/readers`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: device_type, ending_before, expand, limit, location, serial_number, starting_after, status

#### `GET /v1/terminal/readers/{reader}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `error`
  - Filters:
    - `reader` eq `path.reader`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: expand

#### `GET /v1/test_helpers/test_clocks`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, limit, starting_after

#### `GET /v1/topups`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: amount, created, ending_before, expand, limit, starting_after, status

#### `GET /v1/transfers`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: created, destination, ending_before, expand, limit, starting_after, transfer_group

#### `GET /v1/transfers/{id}/reversals`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `error`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, limit, starting_after

#### `GET /v1/treasury/credit_reversals`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, financial_account, limit, received_credit, starting_after, status

#### `GET /v1/treasury/debit_reversals`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, financial_account, limit, received_debit, resolution, starting_after, status

#### `GET /v1/treasury/financial_accounts`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: created, ending_before, expand, limit, starting_after

#### `GET /v1/treasury/inbound_transfers`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, financial_account, limit, starting_after, status

#### `GET /v1/treasury/outbound_payments`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: created, customer, ending_before, expand, financial_account, limit, starting_after, status

#### `GET /v1/treasury/outbound_transfers`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, financial_account, limit, starting_after, status

#### `GET /v1/treasury/received_credits`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, financial_account, limit, linked_flows, starting_after, status

#### `GET /v1/treasury/received_debits`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, financial_account, limit, starting_after, status

#### `GET /v1/treasury/transaction_entries`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: created, effective_at, ending_before, expand, financial_account, limit, order_by, starting_after, transaction

#### `GET /v1/treasury/transactions`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: created, ending_before, expand, financial_account, limit, order_by, starting_after, status, status_transitions

#### `GET /v1/webhook_endpoints`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `error`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: ending_before, expand, limit, starting_after

#### `POST /v1/customers/{customer}/bank_accounts/{id}`
**Status:** planned

**Operations:**
- **create**
  - Component: `error`
  - Filters:
    - `customer` eq `path.customer`
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: customer, id

#### `POST /v1/customers/{customer}/cards/{id}`
**Status:** planned

**Operations:**
- **create**
  - Component: `error`
  - Filters:
    - `customer` eq `path.customer`
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: customer, id

#### `POST /v1/customers/{customer}/sources/{id}`
**Status:** planned

**Operations:**
- **create**
  - Component: `error`
  - Filters:
    - `customer` eq `path.customer`
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: customer, id

#### `POST /v1/terminal/configurations/{configuration}`
**Status:** planned

**Operations:**
- **create**
  - Component: `error`
  - Filters:
    - `configuration` eq `path.configuration`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: configuration

#### `POST /v1/terminal/locations/{location}`
**Status:** planned

**Operations:**
- **create**
  - Component: `error`
  - Filters:
    - `location` eq `path.location`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: location

#### `POST /v1/terminal/readers/{reader}`
**Status:** planned

**Operations:**
- **create**
  - Component: `error`
  - Filters:
    - `reader` eq `path.reader`
  - Notes:
    - Response body references #/components/schemas/error
    - Query parameters: reader

### Component: `event`

#### `GET /v1/events/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `event`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/event
    - Query parameters: expand

### Component: `exchange_rate`

#### `GET /v1/exchange_rates/{rate_id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `exchange_rate`
  - Filters:
    - `rate_id` eq `path.rate_id`
  - Notes:
    - Response body references #/components/schemas/exchange_rate
    - Query parameters: expand

### Component: `external_account`

#### `GET /v1/accounts/{account}/bank_accounts/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `external_account`
  - Filters:
    - `account` eq `path.account`
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/external_account
    - Query parameters: expand

#### `GET /v1/accounts/{account}/external_accounts/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `external_account`
  - Filters:
    - `account` eq `path.account`
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/external_account
    - Query parameters: expand

#### `POST /v1/accounts/{account}/bank_accounts`
**Status:** planned

**Operations:**
- **create**
  - Component: `external_account`
  - Filters:
    - `account` eq `path.account`
  - Notes:
    - Response body references #/components/schemas/external_account
    - Query parameters: account

#### `POST /v1/accounts/{account}/bank_accounts/{id}`
**Status:** planned

**Operations:**
- **create**
  - Component: `external_account`
  - Filters:
    - `account` eq `path.account`
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/external_account
    - Query parameters: account, id

#### `POST /v1/accounts/{account}/external_accounts`
**Status:** planned

**Operations:**
- **create**
  - Component: `external_account`
  - Filters:
    - `account` eq `path.account`
  - Notes:
    - Response body references #/components/schemas/external_account
    - Query parameters: account

#### `POST /v1/accounts/{account}/external_accounts/{id}`
**Status:** planned

**Operations:**
- **create**
  - Component: `external_account`
  - Filters:
    - `account` eq `path.account`
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/external_account
    - Query parameters: account, id

### Component: `fee_refund`

#### `GET /v1/application_fees/{fee}/refunds/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `fee_refund`
  - Filters:
    - `fee` eq `path.fee`
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/fee_refund
    - Query parameters: expand

#### `POST /v1/application_fees/{fee}/refunds/{id}`
**Status:** planned

**Operations:**
- **create**
  - Component: `fee_refund`
  - Filters:
    - `fee` eq `path.fee`
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/fee_refund
    - Query parameters: fee, id

#### `POST /v1/application_fees/{id}/refunds`
**Status:** planned

**Operations:**
- **create**
  - Component: `fee_refund`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/fee_refund
    - Query parameters: id

### Component: `file`

#### `GET /v1/files/{file}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `file`
  - Filters:
    - `filename` eq `path.file`
  - Notes:
    - Response body references #/components/schemas/file
    - Query parameters: expand

#### `POST /v1/files`
**Status:** planned

**Operations:**
- **create**
  - Component: `file`
  - Notes:
    - Response body references #/components/schemas/file

### Component: `file_link`

#### `GET /v1/file_links/{link}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `file_link`
  - Filters:
    - `link` eq `path.link`
  - Notes:
    - Response body references #/components/schemas/file_link
    - Query parameters: expand

#### `POST /v1/file_links`
**Status:** planned

**Operations:**
- **create**
  - Component: `file_link`
  - Notes:
    - Response body references #/components/schemas/file_link

#### `POST /v1/file_links/{link}`
**Status:** planned

**Operations:**
- **create**
  - Component: `file_link`
  - Filters:
    - `link` eq `path.link`
  - Notes:
    - Response body references #/components/schemas/file_link
    - Query parameters: link

### Component: `financial_connections.account`

#### `GET /v1/financial_connections/accounts/{account}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `financial_connections.account`
  - Filters:
    - `account_holder` eq `path.account`
  - Notes:
    - Response body references #/components/schemas/financial_connections.account
    - Query parameters: expand

#### `GET /v1/linked_accounts/{account}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `financial_connections.account`
  - Filters:
    - `account_holder` eq `path.account`
  - Notes:
    - Response body references #/components/schemas/financial_connections.account
    - Query parameters: expand

#### `POST /v1/financial_connections/accounts/{account}/disconnect`
**Status:** planned

**Operations:**
- **create**
  - Component: `financial_connections.account`
  - Filters:
    - `account_holder` eq `path.account`
  - Notes:
    - Response body references #/components/schemas/financial_connections.account
    - Query parameters: account

#### `POST /v1/financial_connections/accounts/{account}/refresh`
**Status:** planned

**Operations:**
- **create**
  - Component: `financial_connections.account`
  - Filters:
    - `account_holder` eq `path.account`
  - Notes:
    - Response body references #/components/schemas/financial_connections.account
    - Query parameters: account

#### `POST /v1/financial_connections/accounts/{account}/subscribe`
**Status:** planned

**Operations:**
- **create**
  - Component: `financial_connections.account`
  - Filters:
    - `account_holder` eq `path.account`
  - Notes:
    - Response body references #/components/schemas/financial_connections.account
    - Query parameters: account

#### `POST /v1/financial_connections/accounts/{account}/unsubscribe`
**Status:** planned

**Operations:**
- **create**
  - Component: `financial_connections.account`
  - Filters:
    - `account_holder` eq `path.account`
  - Notes:
    - Response body references #/components/schemas/financial_connections.account
    - Query parameters: account

#### `POST /v1/linked_accounts/{account}/disconnect`
**Status:** planned

**Operations:**
- **create**
  - Component: `financial_connections.account`
  - Filters:
    - `account_holder` eq `path.account`
  - Notes:
    - Response body references #/components/schemas/financial_connections.account
    - Query parameters: account

#### `POST /v1/linked_accounts/{account}/refresh`
**Status:** planned

**Operations:**
- **create**
  - Component: `financial_connections.account`
  - Filters:
    - `account_holder` eq `path.account`
  - Notes:
    - Response body references #/components/schemas/financial_connections.account
    - Query parameters: account

### Component: `financial_connections.session`

#### `GET /v1/financial_connections/sessions/{session}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `financial_connections.session`
  - Filters:
    - `session` eq `path.session`
  - Notes:
    - Response body references #/components/schemas/financial_connections.session
    - Query parameters: expand

#### `GET /v1/link_account_sessions/{session}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `financial_connections.session`
  - Filters:
    - `session` eq `path.session`
  - Notes:
    - Response body references #/components/schemas/financial_connections.session
    - Query parameters: expand

#### `POST /v1/financial_connections/sessions`
**Status:** planned

**Operations:**
- **create**
  - Component: `financial_connections.session`
  - Notes:
    - Response body references #/components/schemas/financial_connections.session

#### `POST /v1/link_account_sessions`
**Status:** planned

**Operations:**
- **create**
  - Component: `financial_connections.session`
  - Notes:
    - Response body references #/components/schemas/financial_connections.session

### Component: `financial_connections.transaction`

#### `GET /v1/financial_connections/transactions/{transaction}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `financial_connections.transaction`
  - Filters:
    - `transaction_refresh` eq `path.transaction`
  - Notes:
    - Response body references #/components/schemas/financial_connections.transaction
    - Query parameters: expand

### Component: `forwarding.request`

#### `GET /v1/forwarding/requests/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `forwarding.request`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/forwarding.request
    - Query parameters: expand

#### `POST /v1/forwarding/requests`
**Status:** planned

**Operations:**
- **create**
  - Component: `forwarding.request`
  - Notes:
    - Response body references #/components/schemas/forwarding.request

### Component: `funding_instructions`

#### `POST /v1/customers/{customer}/funding_instructions`
**Status:** planned

**Operations:**
- **create**
  - Component: `funding_instructions`
  - Filters:
    - `customer` eq `path.customer`
  - Notes:
    - Response body references #/components/schemas/funding_instructions
    - Query parameters: customer

### Component: `identity.verification_report`

#### `GET /v1/identity/verification_reports/{report}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `identity.verification_report`
  - Filters:
    - `report` eq `path.report`
  - Notes:
    - Response body references #/components/schemas/identity.verification_report
    - Query parameters: expand

### Component: `identity.verification_session`

#### `GET /v1/identity/verification_sessions/{session}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `identity.verification_session`
  - Filters:
    - `session` eq `path.session`
  - Notes:
    - Response body references #/components/schemas/identity.verification_session
    - Query parameters: expand

#### `POST /v1/identity/verification_sessions`
**Status:** planned

**Operations:**
- **create**
  - Component: `identity.verification_session`
  - Notes:
    - Response body references #/components/schemas/identity.verification_session

#### `POST /v1/identity/verification_sessions/{session}`
**Status:** planned

**Operations:**
- **create**
  - Component: `identity.verification_session`
  - Filters:
    - `session` eq `path.session`
  - Notes:
    - Response body references #/components/schemas/identity.verification_session
    - Query parameters: session

#### `POST /v1/identity/verification_sessions/{session}/cancel`
**Status:** planned

**Operations:**
- **create**
  - Component: `identity.verification_session`
  - Filters:
    - `session` eq `path.session`
  - Notes:
    - Response body references #/components/schemas/identity.verification_session
    - Query parameters: session

#### `POST /v1/identity/verification_sessions/{session}/redact`
**Status:** planned

**Operations:**
- **create**
  - Component: `identity.verification_session`
  - Filters:
    - `session` eq `path.session`
  - Notes:
    - Response body references #/components/schemas/identity.verification_session
    - Query parameters: session

### Component: `invoice`

#### `GET /v1/invoices/upcoming`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `invoice`
  - Notes:
    - Response body references #/components/schemas/invoice
    - Query parameters: automatic_tax, coupon, currency, customer, customer_details, discounts, expand, invoice_items, issuer, on_behalf_of, preview_mode, schedule, schedule_details, subscription, subscription_billing_cycle_anchor, subscription_cancel_at, subscription_cancel_at_period_end, subscription_cancel_now, subscription_default_tax_rates, subscription_details, subscription_items, subscription_proration_behavior, subscription_proration_date, subscription_resume_at, subscription_start_date, subscription_trial_end

#### `GET /v1/invoices/{invoice}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `invoice`
  - Filters:
    - `from_invoice` eq `path.invoice`
  - Notes:
    - Response body references #/components/schemas/invoice
    - Query parameters: expand

#### `POST /v1/invoices`
**Status:** planned

**Operations:**
- **create**
  - Component: `invoice`
  - Notes:
    - Response body references #/components/schemas/invoice

#### `POST /v1/invoices/create_preview`
**Status:** planned

**Operations:**
- **create**
  - Component: `invoice`
  - Notes:
    - Response body references #/components/schemas/invoice

#### `POST /v1/invoices/{invoice}`
**Status:** planned

**Operations:**
- **create**
  - Component: `invoice`
  - Filters:
    - `from_invoice` eq `path.invoice`
  - Notes:
    - Response body references #/components/schemas/invoice
    - Query parameters: invoice

#### `POST /v1/invoices/{invoice}/add_lines`
**Status:** planned

**Operations:**
- **create**
  - Component: `invoice`
  - Filters:
    - `from_invoice` eq `path.invoice`
  - Notes:
    - Response body references #/components/schemas/invoice
    - Query parameters: invoice

#### `POST /v1/invoices/{invoice}/finalize`
**Status:** planned

**Operations:**
- **create**
  - Component: `invoice`
  - Filters:
    - `from_invoice` eq `path.invoice`
  - Notes:
    - Response body references #/components/schemas/invoice
    - Query parameters: invoice

#### `POST /v1/invoices/{invoice}/mark_uncollectible`
**Status:** planned

**Operations:**
- **create**
  - Component: `invoice`
  - Filters:
    - `from_invoice` eq `path.invoice`
  - Notes:
    - Response body references #/components/schemas/invoice
    - Query parameters: invoice

#### `POST /v1/invoices/{invoice}/pay`
**Status:** planned

**Operations:**
- **create**
  - Component: `invoice`
  - Filters:
    - `from_invoice` eq `path.invoice`
  - Notes:
    - Response body references #/components/schemas/invoice
    - Query parameters: invoice

#### `POST /v1/invoices/{invoice}/remove_lines`
**Status:** planned

**Operations:**
- **create**
  - Component: `invoice`
  - Filters:
    - `from_invoice` eq `path.invoice`
  - Notes:
    - Response body references #/components/schemas/invoice
    - Query parameters: invoice

#### `POST /v1/invoices/{invoice}/send`
**Status:** planned

**Operations:**
- **create**
  - Component: `invoice`
  - Filters:
    - `from_invoice` eq `path.invoice`
  - Notes:
    - Response body references #/components/schemas/invoice
    - Query parameters: invoice

#### `POST /v1/invoices/{invoice}/update_lines`
**Status:** planned

**Operations:**
- **create**
  - Component: `invoice`
  - Filters:
    - `from_invoice` eq `path.invoice`
  - Notes:
    - Response body references #/components/schemas/invoice
    - Query parameters: invoice

#### `POST /v1/invoices/{invoice}/void`
**Status:** planned

**Operations:**
- **create**
  - Component: `invoice`
  - Filters:
    - `from_invoice` eq `path.invoice`
  - Notes:
    - Response body references #/components/schemas/invoice
    - Query parameters: invoice

### Component: `invoice_rendering_template`

#### `GET /v1/invoice_rendering_templates/{template}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `invoice_rendering_template`
  - Filters:
    - `template` eq `path.template`
  - Notes:
    - Response body references #/components/schemas/invoice_rendering_template
    - Query parameters: expand, version

#### `POST /v1/invoice_rendering_templates/{template}/archive`
**Status:** planned

**Operations:**
- **create**
  - Component: `invoice_rendering_template`
  - Filters:
    - `template` eq `path.template`
  - Notes:
    - Response body references #/components/schemas/invoice_rendering_template
    - Query parameters: template

#### `POST /v1/invoice_rendering_templates/{template}/unarchive`
**Status:** planned

**Operations:**
- **create**
  - Component: `invoice_rendering_template`
  - Filters:
    - `template` eq `path.template`
  - Notes:
    - Response body references #/components/schemas/invoice_rendering_template
    - Query parameters: template

### Component: `invoiceitem`

#### `GET /v1/invoiceitems/{invoiceitem}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `invoiceitem`
  - Filters:
    - `invoiceitem` eq `path.invoiceitem`
  - Notes:
    - Response body references #/components/schemas/invoiceitem
    - Query parameters: expand

#### `POST /v1/invoiceitems`
**Status:** planned

**Operations:**
- **create**
  - Component: `invoiceitem`
  - Notes:
    - Response body references #/components/schemas/invoiceitem

#### `POST /v1/invoiceitems/{invoiceitem}`
**Status:** planned

**Operations:**
- **create**
  - Component: `invoiceitem`
  - Filters:
    - `invoiceitem` eq `path.invoiceitem`
  - Notes:
    - Response body references #/components/schemas/invoiceitem
    - Query parameters: invoiceitem

### Component: `issuing.authorization`

#### `GET /v1/issuing/authorizations/{authorization}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `issuing.authorization`
  - Filters:
    - `authorization_method` eq `path.authorization`
  - Notes:
    - Response body references #/components/schemas/issuing.authorization
    - Query parameters: expand

#### `POST /v1/issuing/authorizations/{authorization}`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.authorization`
  - Filters:
    - `authorization_method` eq `path.authorization`
  - Notes:
    - Response body references #/components/schemas/issuing.authorization
    - Query parameters: authorization

#### `POST /v1/issuing/authorizations/{authorization}/approve`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.authorization`
  - Filters:
    - `authorization_method` eq `path.authorization`
  - Notes:
    - Response body references #/components/schemas/issuing.authorization
    - Query parameters: authorization

#### `POST /v1/issuing/authorizations/{authorization}/decline`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.authorization`
  - Filters:
    - `authorization_method` eq `path.authorization`
  - Notes:
    - Response body references #/components/schemas/issuing.authorization
    - Query parameters: authorization

#### `POST /v1/test_helpers/issuing/authorizations`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.authorization`
  - Notes:
    - Response body references #/components/schemas/issuing.authorization

#### `POST /v1/test_helpers/issuing/authorizations/{authorization}/capture`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.authorization`
  - Filters:
    - `authorization_method` eq `path.authorization`
  - Notes:
    - Response body references #/components/schemas/issuing.authorization
    - Query parameters: authorization

#### `POST /v1/test_helpers/issuing/authorizations/{authorization}/expire`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.authorization`
  - Filters:
    - `authorization_method` eq `path.authorization`
  - Notes:
    - Response body references #/components/schemas/issuing.authorization
    - Query parameters: authorization

#### `POST /v1/test_helpers/issuing/authorizations/{authorization}/finalize_amount`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.authorization`
  - Filters:
    - `authorization_method` eq `path.authorization`
  - Notes:
    - Response body references #/components/schemas/issuing.authorization
    - Query parameters: authorization

#### `POST /v1/test_helpers/issuing/authorizations/{authorization}/increment`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.authorization`
  - Filters:
    - `authorization_method` eq `path.authorization`
  - Notes:
    - Response body references #/components/schemas/issuing.authorization
    - Query parameters: authorization

#### `POST /v1/test_helpers/issuing/authorizations/{authorization}/reverse`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.authorization`
  - Filters:
    - `authorization_method` eq `path.authorization`
  - Notes:
    - Response body references #/components/schemas/issuing.authorization
    - Query parameters: authorization

### Component: `issuing.card`

#### `GET /v1/issuing/cards/{card}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `issuing.card`
  - Filters:
    - `cardholder` eq `path.card`
  - Notes:
    - Response body references #/components/schemas/issuing.card
    - Query parameters: expand

#### `POST /v1/issuing/cards`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.card`
  - Notes:
    - Response body references #/components/schemas/issuing.card

#### `POST /v1/issuing/cards/{card}`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.card`
  - Filters:
    - `cardholder` eq `path.card`
  - Notes:
    - Response body references #/components/schemas/issuing.card
    - Query parameters: card

#### `POST /v1/test_helpers/issuing/cards/{card}/shipping/deliver`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.card`
  - Filters:
    - `cardholder` eq `path.card`
  - Notes:
    - Response body references #/components/schemas/issuing.card
    - Query parameters: card

#### `POST /v1/test_helpers/issuing/cards/{card}/shipping/fail`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.card`
  - Filters:
    - `cardholder` eq `path.card`
  - Notes:
    - Response body references #/components/schemas/issuing.card
    - Query parameters: card

#### `POST /v1/test_helpers/issuing/cards/{card}/shipping/return`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.card`
  - Filters:
    - `cardholder` eq `path.card`
  - Notes:
    - Response body references #/components/schemas/issuing.card
    - Query parameters: card

#### `POST /v1/test_helpers/issuing/cards/{card}/shipping/ship`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.card`
  - Filters:
    - `cardholder` eq `path.card`
  - Notes:
    - Response body references #/components/schemas/issuing.card
    - Query parameters: card

### Component: `issuing.cardholder`

#### `GET /v1/issuing/cardholders/{cardholder}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `issuing.cardholder`
  - Filters:
    - `cardholder` eq `path.cardholder`
  - Notes:
    - Response body references #/components/schemas/issuing.cardholder
    - Query parameters: expand

#### `POST /v1/issuing/cardholders`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.cardholder`
  - Notes:
    - Response body references #/components/schemas/issuing.cardholder

#### `POST /v1/issuing/cardholders/{cardholder}`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.cardholder`
  - Filters:
    - `cardholder` eq `path.cardholder`
  - Notes:
    - Response body references #/components/schemas/issuing.cardholder
    - Query parameters: cardholder

### Component: `issuing.dispute`

#### `GET /v1/issuing/disputes/{dispute}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `issuing.dispute`
  - Filters:
    - `dispute` eq `path.dispute`
  - Notes:
    - Response body references #/components/schemas/issuing.dispute
    - Query parameters: expand

#### `POST /v1/issuing/disputes`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.dispute`
  - Notes:
    - Response body references #/components/schemas/issuing.dispute

#### `POST /v1/issuing/disputes/{dispute}`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.dispute`
  - Filters:
    - `dispute` eq `path.dispute`
  - Notes:
    - Response body references #/components/schemas/issuing.dispute
    - Query parameters: dispute

#### `POST /v1/issuing/disputes/{dispute}/submit`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.dispute`
  - Filters:
    - `dispute` eq `path.dispute`
  - Notes:
    - Response body references #/components/schemas/issuing.dispute
    - Query parameters: dispute

### Component: `issuing.personalization_design`

#### `GET /v1/issuing/personalization_designs/{personalization_design}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `issuing.personalization_design`
  - Filters:
    - `personalization_design` eq `path.personalization_design`
  - Notes:
    - Response body references #/components/schemas/issuing.personalization_design
    - Query parameters: expand

#### `POST /v1/issuing/personalization_designs`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.personalization_design`
  - Notes:
    - Response body references #/components/schemas/issuing.personalization_design

#### `POST /v1/issuing/personalization_designs/{personalization_design}`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.personalization_design`
  - Filters:
    - `personalization_design` eq `path.personalization_design`
  - Notes:
    - Response body references #/components/schemas/issuing.personalization_design
    - Query parameters: personalization_design

#### `POST /v1/test_helpers/issuing/personalization_designs/{personalization_design}/activate`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.personalization_design`
  - Filters:
    - `personalization_design` eq `path.personalization_design`
  - Notes:
    - Response body references #/components/schemas/issuing.personalization_design
    - Query parameters: personalization_design

#### `POST /v1/test_helpers/issuing/personalization_designs/{personalization_design}/deactivate`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.personalization_design`
  - Filters:
    - `personalization_design` eq `path.personalization_design`
  - Notes:
    - Response body references #/components/schemas/issuing.personalization_design
    - Query parameters: personalization_design

#### `POST /v1/test_helpers/issuing/personalization_designs/{personalization_design}/reject`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.personalization_design`
  - Filters:
    - `personalization_design` eq `path.personalization_design`
  - Notes:
    - Response body references #/components/schemas/issuing.personalization_design
    - Query parameters: personalization_design

### Component: `issuing.physical_bundle`

#### `GET /v1/issuing/physical_bundles/{physical_bundle}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `issuing.physical_bundle`
  - Filters:
    - `physical_bundle` eq `path.physical_bundle`
  - Notes:
    - Response body references #/components/schemas/issuing.physical_bundle
    - Query parameters: expand

### Component: `issuing.settlement`

#### `GET /v1/issuing/settlements/{settlement}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `issuing.settlement`
  - Filters:
    - `network_settlement_identifier` eq `path.settlement`
  - Notes:
    - Response body references #/components/schemas/issuing.settlement
    - Query parameters: expand

#### `POST /v1/issuing/settlements/{settlement}`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.settlement`
  - Filters:
    - `network_settlement_identifier` eq `path.settlement`
  - Notes:
    - Response body references #/components/schemas/issuing.settlement
    - Query parameters: settlement

#### `POST /v1/test_helpers/issuing/settlements`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.settlement`
  - Notes:
    - Response body references #/components/schemas/issuing.settlement

### Component: `issuing.token`

#### `GET /v1/issuing/tokens/{token}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `issuing.token`
  - Filters:
    - `token` eq `path.token`
  - Notes:
    - Response body references #/components/schemas/issuing.token
    - Query parameters: expand

#### `POST /v1/issuing/tokens/{token}`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.token`
  - Filters:
    - `token` eq `path.token`
  - Notes:
    - Response body references #/components/schemas/issuing.token
    - Query parameters: token

### Component: `issuing.transaction`

#### `GET /v1/issuing/transactions/{transaction}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `issuing.transaction`
  - Filters:
    - `balance_transaction` eq `path.transaction`
  - Notes:
    - Response body references #/components/schemas/issuing.transaction
    - Query parameters: expand

#### `POST /v1/issuing/transactions/{transaction}`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.transaction`
  - Filters:
    - `balance_transaction` eq `path.transaction`
  - Notes:
    - Response body references #/components/schemas/issuing.transaction
    - Query parameters: transaction

#### `POST /v1/test_helpers/issuing/transactions/create_force_capture`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.transaction`
  - Notes:
    - Response body references #/components/schemas/issuing.transaction

#### `POST /v1/test_helpers/issuing/transactions/create_unlinked_refund`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.transaction`
  - Notes:
    - Response body references #/components/schemas/issuing.transaction

#### `POST /v1/test_helpers/issuing/transactions/{transaction}/refund`
**Status:** planned

**Operations:**
- **create**
  - Component: `issuing.transaction`
  - Filters:
    - `balance_transaction` eq `path.transaction`
  - Notes:
    - Response body references #/components/schemas/issuing.transaction
    - Query parameters: transaction

### Component: `line_item`

#### `POST /v1/invoices/{invoice}/lines/{line_item_id}`
**Status:** planned

**Operations:**
- **create**
  - Component: `line_item`
  - Filters:
    - `invoice` eq `path.invoice`
    - `line_item_id` eq `path.line_item_id`
  - Notes:
    - Response body references #/components/schemas/line_item
    - Query parameters: invoice, line_item_id

### Component: `login_link`

#### `POST /v1/accounts/{account}/login_links`
**Status:** planned

**Operations:**
- **create**
  - Component: `login_link`
  - Filters:
    - `account` eq `path.account`
  - Notes:
    - Response body references #/components/schemas/login_link
    - Query parameters: account

### Component: `mandate`

#### `GET /v1/mandates/{mandate}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `mandate`
  - Filters:
    - `mandate` eq `path.mandate`
  - Notes:
    - Response body references #/components/schemas/mandate
    - Query parameters: expand

### Component: `payment_intent`

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

### Component: `payment_link`

#### `GET /v1/payment_links/{payment_link}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `payment_link`
  - Filters:
    - `payment_link` eq `path.payment_link`
  - Notes:
    - Response body references #/components/schemas/payment_link
    - Query parameters: expand

#### `POST /v1/payment_links`
**Status:** planned

**Operations:**
- **create**
  - Component: `payment_link`
  - Notes:
    - Response body references #/components/schemas/payment_link

#### `POST /v1/payment_links/{payment_link}`
**Status:** planned

**Operations:**
- **create**
  - Component: `payment_link`
  - Filters:
    - `payment_link` eq `path.payment_link`
  - Notes:
    - Response body references #/components/schemas/payment_link
    - Query parameters: payment_link

### Component: `payment_method`

#### `GET /v1/customers/{customer}/payment_methods/{payment_method}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `payment_method`
  - Filters:
    - `customer` eq `path.customer`
    - `payment_method` eq `path.payment_method`
  - Notes:
    - Response body references #/components/schemas/payment_method
    - Query parameters: expand

#### `GET /v1/payment_methods/{payment_method}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `payment_method`
  - Filters:
    - `payment_method` eq `path.payment_method`
  - Notes:
    - Response body references #/components/schemas/payment_method
    - Query parameters: expand

#### `POST /v1/payment_methods`
**Status:** planned

**Operations:**
- **create**
  - Component: `payment_method`
  - Notes:
    - Response body references #/components/schemas/payment_method

#### `POST /v1/payment_methods/{payment_method}`
**Status:** planned

**Operations:**
- **create**
  - Component: `payment_method`
  - Filters:
    - `payment_method` eq `path.payment_method`
  - Notes:
    - Response body references #/components/schemas/payment_method
    - Query parameters: payment_method

#### `POST /v1/payment_methods/{payment_method}/attach`
**Status:** planned

**Operations:**
- **create**
  - Component: `payment_method`
  - Filters:
    - `payment_method` eq `path.payment_method`
  - Notes:
    - Response body references #/components/schemas/payment_method
    - Query parameters: payment_method

#### `POST /v1/payment_methods/{payment_method}/detach`
**Status:** planned

**Operations:**
- **create**
  - Component: `payment_method`
  - Filters:
    - `payment_method` eq `path.payment_method`
  - Notes:
    - Response body references #/components/schemas/payment_method
    - Query parameters: payment_method

### Component: `payment_method_configuration`

#### `GET /v1/payment_method_configurations/{configuration}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `payment_method_configuration`
  - Filters:
    - `configuration` eq `path.configuration`
  - Notes:
    - Response body references #/components/schemas/payment_method_configuration
    - Query parameters: expand

#### `POST /v1/payment_method_configurations`
**Status:** planned

**Operations:**
- **create**
  - Component: `payment_method_configuration`
  - Notes:
    - Response body references #/components/schemas/payment_method_configuration

#### `POST /v1/payment_method_configurations/{configuration}`
**Status:** planned

**Operations:**
- **create**
  - Component: `payment_method_configuration`
  - Filters:
    - `configuration` eq `path.configuration`
  - Notes:
    - Response body references #/components/schemas/payment_method_configuration
    - Query parameters: configuration

### Component: `payment_method_domain`

#### `GET /v1/payment_method_domains/{payment_method_domain}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `payment_method_domain`
  - Filters:
    - `payment_method_domain` eq `path.payment_method_domain`
  - Notes:
    - Response body references #/components/schemas/payment_method_domain
    - Query parameters: expand

#### `POST /v1/payment_method_domains`
**Status:** planned

**Operations:**
- **create**
  - Component: `payment_method_domain`
  - Notes:
    - Response body references #/components/schemas/payment_method_domain

#### `POST /v1/payment_method_domains/{payment_method_domain}`
**Status:** planned

**Operations:**
- **create**
  - Component: `payment_method_domain`
  - Filters:
    - `payment_method_domain` eq `path.payment_method_domain`
  - Notes:
    - Response body references #/components/schemas/payment_method_domain
    - Query parameters: payment_method_domain

#### `POST /v1/payment_method_domains/{payment_method_domain}/validate`
**Status:** planned

**Operations:**
- **create**
  - Component: `payment_method_domain`
  - Filters:
    - `payment_method_domain` eq `path.payment_method_domain`
  - Notes:
    - Response body references #/components/schemas/payment_method_domain
    - Query parameters: payment_method_domain

### Component: `payment_source`

#### `GET /v1/customers/{customer}/sources/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `payment_source`
  - Filters:
    - `customer` eq `path.customer`
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/payment_source
    - Query parameters: expand

#### `POST /v1/customers/{customer}/bank_accounts`
**Status:** planned

**Operations:**
- **create**
  - Component: `payment_source`
  - Filters:
    - `customer` eq `path.customer`
  - Notes:
    - Response body references #/components/schemas/payment_source
    - Query parameters: customer

#### `POST /v1/customers/{customer}/cards`
**Status:** planned

**Operations:**
- **create**
  - Component: `payment_source`
  - Filters:
    - `customer` eq `path.customer`
  - Notes:
    - Response body references #/components/schemas/payment_source
    - Query parameters: customer

#### `POST /v1/customers/{customer}/sources`
**Status:** planned

**Operations:**
- **create**
  - Component: `payment_source`
  - Filters:
    - `customer` eq `path.customer`
  - Notes:
    - Response body references #/components/schemas/payment_source
    - Query parameters: customer

### Component: `payout`

#### `GET /v1/payouts/{payout}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `payout`
  - Filters:
    - `original_payout` eq `path.payout`
  - Notes:
    - Response body references #/components/schemas/payout
    - Query parameters: expand

#### `POST /v1/payouts`
**Status:** planned

**Operations:**
- **create**
  - Component: `payout`
  - Notes:
    - Response body references #/components/schemas/payout

#### `POST /v1/payouts/{payout}`
**Status:** planned

**Operations:**
- **create**
  - Component: `payout`
  - Filters:
    - `original_payout` eq `path.payout`
  - Notes:
    - Response body references #/components/schemas/payout
    - Query parameters: payout

#### `POST /v1/payouts/{payout}/cancel`
**Status:** planned

**Operations:**
- **create**
  - Component: `payout`
  - Filters:
    - `original_payout` eq `path.payout`
  - Notes:
    - Response body references #/components/schemas/payout
    - Query parameters: payout

#### `POST /v1/payouts/{payout}/reverse`
**Status:** planned

**Operations:**
- **create**
  - Component: `payout`
  - Filters:
    - `original_payout` eq `path.payout`
  - Notes:
    - Response body references #/components/schemas/payout
    - Query parameters: payout

### Component: `person`

#### `GET /v1/accounts/{account}/people/{person}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `person`
  - Filters:
    - `account` eq `path.account`
    - `person` eq `path.person`
  - Notes:
    - Response body references #/components/schemas/person
    - Query parameters: expand

#### `GET /v1/accounts/{account}/persons/{person}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `person`
  - Filters:
    - `account` eq `path.account`
    - `person` eq `path.person`
  - Notes:
    - Response body references #/components/schemas/person
    - Query parameters: expand

#### `POST /v1/accounts/{account}/people`
**Status:** planned

**Operations:**
- **create**
  - Component: `person`
  - Filters:
    - `account` eq `path.account`
  - Notes:
    - Response body references #/components/schemas/person
    - Query parameters: account

#### `POST /v1/accounts/{account}/people/{person}`
**Status:** planned

**Operations:**
- **create**
  - Component: `person`
  - Filters:
    - `account` eq `path.account`
    - `person` eq `path.person`
  - Notes:
    - Response body references #/components/schemas/person
    - Query parameters: account, person

#### `POST /v1/accounts/{account}/persons`
**Status:** planned

**Operations:**
- **create**
  - Component: `person`
  - Filters:
    - `account` eq `path.account`
  - Notes:
    - Response body references #/components/schemas/person
    - Query parameters: account

#### `POST /v1/accounts/{account}/persons/{person}`
**Status:** planned

**Operations:**
- **create**
  - Component: `person`
  - Filters:
    - `account` eq `path.account`
    - `person` eq `path.person`
  - Notes:
    - Response body references #/components/schemas/person
    - Query parameters: account, person

### Component: `plan`

#### `GET /v1/plans/{plan}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `plan`
  - Filters:
    - `plan` eq `path.plan`
  - Notes:
    - Response body references #/components/schemas/plan
    - Query parameters: expand

#### `POST /v1/plans`
**Status:** planned

**Operations:**
- **create**
  - Component: `plan`
  - Notes:
    - Response body references #/components/schemas/plan

#### `POST /v1/plans/{plan}`
**Status:** planned

**Operations:**
- **create**
  - Component: `plan`
  - Filters:
    - `plan` eq `path.plan`
  - Notes:
    - Response body references #/components/schemas/plan
    - Query parameters: plan

### Component: `price`

#### `GET /v1/prices/{price}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `price`
  - Filters:
    - `price` eq `path.price`
  - Notes:
    - Response body references #/components/schemas/price
    - Query parameters: expand

#### `POST /v1/prices`
**Status:** planned

**Operations:**
- **create**
  - Component: `price`
  - Notes:
    - Response body references #/components/schemas/price

#### `POST /v1/prices/{price}`
**Status:** planned

**Operations:**
- **create**
  - Component: `price`
  - Filters:
    - `price` eq `path.price`
  - Notes:
    - Response body references #/components/schemas/price
    - Query parameters: price

### Component: `product`

#### `GET /v1/products/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `product`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/product
    - Query parameters: expand

#### `POST /v1/products`
**Status:** planned

**Operations:**
- **create**
  - Component: `product`
  - Notes:
    - Response body references #/components/schemas/product

#### `POST /v1/products/{id}`
**Status:** planned

**Operations:**
- **create**
  - Component: `product`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/product
    - Query parameters: id

### Component: `product_feature`

#### `GET /v1/products/{product}/features/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `product_feature`
  - Filters:
    - `id` eq `path.id`
    - `product` eq `path.product`
  - Notes:
    - Response body references #/components/schemas/product_feature
    - Query parameters: expand

#### `POST /v1/products/{product}/features`
**Status:** planned

**Operations:**
- **create**
  - Component: `product_feature`
  - Filters:
    - `product` eq `path.product`
  - Notes:
    - Response body references #/components/schemas/product_feature
    - Query parameters: product

### Component: `promotion_code`

#### `GET /v1/promotion_codes/{promotion_code}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `promotion_code`
  - Filters:
    - `promotion_code` eq `path.promotion_code`
  - Notes:
    - Response body references #/components/schemas/promotion_code
    - Query parameters: expand

#### `POST /v1/promotion_codes`
**Status:** planned

**Operations:**
- **create**
  - Component: `promotion_code`
  - Notes:
    - Response body references #/components/schemas/promotion_code

#### `POST /v1/promotion_codes/{promotion_code}`
**Status:** planned

**Operations:**
- **create**
  - Component: `promotion_code`
  - Filters:
    - `promotion_code` eq `path.promotion_code`
  - Notes:
    - Response body references #/components/schemas/promotion_code
    - Query parameters: promotion_code

### Component: `quote`

#### `GET /v1/quotes/{quote}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `quote`
  - Filters:
    - `from_quote` eq `path.quote`
  - Notes:
    - Response body references #/components/schemas/quote
    - Query parameters: expand

#### `POST /v1/quotes`
**Status:** planned

**Operations:**
- **create**
  - Component: `quote`
  - Notes:
    - Response body references #/components/schemas/quote

#### `POST /v1/quotes/{quote}`
**Status:** planned

**Operations:**
- **create**
  - Component: `quote`
  - Filters:
    - `from_quote` eq `path.quote`
  - Notes:
    - Response body references #/components/schemas/quote
    - Query parameters: quote

#### `POST /v1/quotes/{quote}/accept`
**Status:** planned

**Operations:**
- **create**
  - Component: `quote`
  - Filters:
    - `from_quote` eq `path.quote`
  - Notes:
    - Response body references #/components/schemas/quote
    - Query parameters: quote

#### `POST /v1/quotes/{quote}/cancel`
**Status:** planned

**Operations:**
- **create**
  - Component: `quote`
  - Filters:
    - `from_quote` eq `path.quote`
  - Notes:
    - Response body references #/components/schemas/quote
    - Query parameters: quote

#### `POST /v1/quotes/{quote}/finalize`
**Status:** planned

**Operations:**
- **create**
  - Component: `quote`
  - Filters:
    - `from_quote` eq `path.quote`
  - Notes:
    - Response body references #/components/schemas/quote
    - Query parameters: quote

### Component: `radar.early_fraud_warning`

#### `GET /v1/radar/early_fraud_warnings/{early_fraud_warning}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `radar.early_fraud_warning`
  - Filters:
    - `early_fraud_warning` eq `path.early_fraud_warning`
  - Notes:
    - Response body references #/components/schemas/radar.early_fraud_warning
    - Query parameters: expand

### Component: `radar.value_list`

#### `GET /v1/radar/value_lists/{value_list}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `radar.value_list`
  - Filters:
    - `value_list` eq `path.value_list`
  - Notes:
    - Response body references #/components/schemas/radar.value_list
    - Query parameters: expand

#### `POST /v1/radar/value_lists`
**Status:** planned

**Operations:**
- **create**
  - Component: `radar.value_list`
  - Notes:
    - Response body references #/components/schemas/radar.value_list

#### `POST /v1/radar/value_lists/{value_list}`
**Status:** planned

**Operations:**
- **create**
  - Component: `radar.value_list`
  - Filters:
    - `value_list` eq `path.value_list`
  - Notes:
    - Response body references #/components/schemas/radar.value_list
    - Query parameters: value_list

### Component: `radar.value_list_item`

#### `GET /v1/radar/value_list_items/{item}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `radar.value_list_item`
  - Filters:
    - `item` eq `path.item`
  - Notes:
    - Response body references #/components/schemas/radar.value_list_item
    - Query parameters: expand

#### `POST /v1/radar/value_list_items`
**Status:** planned

**Operations:**
- **create**
  - Component: `radar.value_list_item`
  - Notes:
    - Response body references #/components/schemas/radar.value_list_item

### Component: `refund`

#### `GET /v1/charges/{charge}/refunds/{refund}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `refund`
  - Filters:
    - `charge` eq `path.charge`
    - `refund` eq `path.refund`
  - Notes:
    - Response body references #/components/schemas/refund
    - Query parameters: expand

#### `GET /v1/refunds/{refund}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `refund`
  - Filters:
    - `refund` eq `path.refund`
  - Notes:
    - Response body references #/components/schemas/refund
    - Query parameters: expand

#### `POST /v1/charges/{charge}/refunds`
**Status:** planned

**Operations:**
- **create**
  - Component: `refund`
  - Filters:
    - `charge` eq `path.charge`
  - Notes:
    - Response body references #/components/schemas/refund
    - Query parameters: charge

#### `POST /v1/charges/{charge}/refunds/{refund}`
**Status:** planned

**Operations:**
- **create**
  - Component: `refund`
  - Filters:
    - `charge` eq `path.charge`
    - `refund` eq `path.refund`
  - Notes:
    - Response body references #/components/schemas/refund
    - Query parameters: charge, refund

#### `POST /v1/refunds`
**Status:** planned

**Operations:**
- **create**
  - Component: `refund`
  - Notes:
    - Response body references #/components/schemas/refund

#### `POST /v1/refunds/{refund}`
**Status:** planned

**Operations:**
- **create**
  - Component: `refund`
  - Filters:
    - `refund` eq `path.refund`
  - Notes:
    - Response body references #/components/schemas/refund
    - Query parameters: refund

#### `POST /v1/refunds/{refund}/cancel`
**Status:** planned

**Operations:**
- **create**
  - Component: `refund`
  - Filters:
    - `refund` eq `path.refund`
  - Notes:
    - Response body references #/components/schemas/refund
    - Query parameters: refund

#### `POST /v1/test_helpers/refunds/{refund}/expire`
**Status:** planned

**Operations:**
- **create**
  - Component: `refund`
  - Filters:
    - `refund` eq `path.refund`
  - Notes:
    - Response body references #/components/schemas/refund
    - Query parameters: refund

### Component: `reporting.report_run`

#### `GET /v1/reporting/report_runs/{report_run}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `reporting.report_run`
  - Filters:
    - `report_run` eq `path.report_run`
  - Notes:
    - Response body references #/components/schemas/reporting.report_run
    - Query parameters: expand

#### `POST /v1/reporting/report_runs`
**Status:** planned

**Operations:**
- **create**
  - Component: `reporting.report_run`
  - Notes:
    - Response body references #/components/schemas/reporting.report_run

### Component: `reporting.report_type`

#### `GET /v1/reporting/report_types/{report_type}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `reporting.report_type`
  - Filters:
    - `report_type` eq `path.report_type`
  - Notes:
    - Response body references #/components/schemas/reporting.report_type
    - Query parameters: expand

### Component: `review`

#### `GET /v1/reviews/{review}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `review`
  - Filters:
    - `review` eq `path.review`
  - Notes:
    - Response body references #/components/schemas/review
    - Query parameters: expand

#### `POST /v1/reviews/{review}/approve`
**Status:** planned

**Operations:**
- **create**
  - Component: `review`
  - Filters:
    - `review` eq `path.review`
  - Notes:
    - Response body references #/components/schemas/review
    - Query parameters: review

### Component: `scheduled_query_run`

#### `GET /v1/sigma/scheduled_query_runs/{scheduled_query_run}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `scheduled_query_run`
  - Filters:
    - `scheduled_query_run` eq `path.scheduled_query_run`
  - Notes:
    - Response body references #/components/schemas/scheduled_query_run
    - Query parameters: expand

### Component: `setup_intent`

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

### Component: `shipping_rate`

#### `GET /v1/shipping_rates/{shipping_rate_token}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `shipping_rate`
  - Filters:
    - `shipping_rate_token` eq `path.shipping_rate_token`
  - Notes:
    - Response body references #/components/schemas/shipping_rate
    - Query parameters: expand

#### `POST /v1/shipping_rates`
**Status:** planned

**Operations:**
- **create**
  - Component: `shipping_rate`
  - Notes:
    - Response body references #/components/schemas/shipping_rate

#### `POST /v1/shipping_rates/{shipping_rate_token}`
**Status:** planned

**Operations:**
- **create**
  - Component: `shipping_rate`
  - Filters:
    - `shipping_rate_token` eq `path.shipping_rate_token`
  - Notes:
    - Response body references #/components/schemas/shipping_rate
    - Query parameters: shipping_rate_token

### Component: `source`

#### `GET /v1/sources/{source}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `source`
  - Filters:
    - `source_order` eq `path.source`
  - Notes:
    - Response body references #/components/schemas/source
    - Query parameters: client_secret, expand

#### `POST /v1/sources`
**Status:** planned

**Operations:**
- **create**
  - Component: `source`
  - Notes:
    - Response body references #/components/schemas/source

#### `POST /v1/sources/{source}`
**Status:** planned

**Operations:**
- **create**
  - Component: `source`
  - Filters:
    - `source_order` eq `path.source`
  - Notes:
    - Response body references #/components/schemas/source
    - Query parameters: source

#### `POST /v1/sources/{source}/verify`
**Status:** planned

**Operations:**
- **create**
  - Component: `source`
  - Filters:
    - `source_order` eq `path.source`
  - Notes:
    - Response body references #/components/schemas/source
    - Query parameters: source

### Component: `source_mandate_notification`

#### `GET /v1/sources/{source}/mandate_notifications/{mandate_notification}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `source_mandate_notification`
  - Filters:
    - `mandate_notification` eq `path.mandate_notification`
    - `source` eq `path.source`
  - Notes:
    - Response body references #/components/schemas/source_mandate_notification
    - Query parameters: expand

### Component: `source_transaction`

#### `GET /v1/sources/{source}/source_transactions/{source_transaction}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `source_transaction`
  - Filters:
    - `source` eq `path.source`
    - `source_transaction` eq `path.source_transaction`
  - Notes:
    - Response body references #/components/schemas/source_transaction
    - Query parameters: expand

### Component: `subscription`

#### `DELETE /v1/customers/{customer}/subscriptions/{subscription_exposed_id}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `subscription`
  - Filters:
    - `customer` eq `path.customer`
    - `subscription_exposed_id` eq `path.subscription_exposed_id`
  - Notes:
    - Response body references #/components/schemas/subscription
    - Query parameters: customer, subscription_exposed_id

#### `DELETE /v1/subscriptions/{subscription_exposed_id}`
**Status:** planned

**Operations:**
- **delete**
  - Component: `subscription`
  - Filters:
    - `subscription_exposed_id` eq `path.subscription_exposed_id`
  - Notes:
    - Response body references #/components/schemas/subscription
    - Query parameters: subscription_exposed_id

#### `GET /v1/customers/{customer}/subscriptions/{subscription_exposed_id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `subscription`
  - Filters:
    - `customer` eq `path.customer`
    - `subscription_exposed_id` eq `path.subscription_exposed_id`
  - Notes:
    - Response body references #/components/schemas/subscription
    - Query parameters: expand

#### `GET /v1/subscriptions/{subscription_exposed_id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `subscription`
  - Filters:
    - `subscription_exposed_id` eq `path.subscription_exposed_id`
  - Notes:
    - Response body references #/components/schemas/subscription
    - Query parameters: expand

#### `POST /v1/customers/{customer}/subscriptions`
**Status:** planned

**Operations:**
- **create**
  - Component: `subscription`
  - Filters:
    - `customer` eq `path.customer`
  - Notes:
    - Response body references #/components/schemas/subscription
    - Query parameters: customer

#### `POST /v1/customers/{customer}/subscriptions/{subscription_exposed_id}`
**Status:** planned

**Operations:**
- **create**
  - Component: `subscription`
  - Filters:
    - `customer` eq `path.customer`
    - `subscription_exposed_id` eq `path.subscription_exposed_id`
  - Notes:
    - Response body references #/components/schemas/subscription
    - Query parameters: customer, subscription_exposed_id

#### `POST /v1/subscriptions`
**Status:** planned

**Operations:**
- **create**
  - Component: `subscription`
  - Notes:
    - Response body references #/components/schemas/subscription

#### `POST /v1/subscriptions/{subscription_exposed_id}`
**Status:** planned

**Operations:**
- **create**
  - Component: `subscription`
  - Filters:
    - `subscription_exposed_id` eq `path.subscription_exposed_id`
  - Notes:
    - Response body references #/components/schemas/subscription
    - Query parameters: subscription_exposed_id

#### `POST /v1/subscriptions/{subscription}/resume`
**Status:** planned

**Operations:**
- **create**
  - Component: `subscription`
  - Filters:
    - `subscription` eq `path.subscription`
  - Notes:
    - Response body references #/components/schemas/subscription
    - Query parameters: subscription

### Component: `subscription_item`

#### `GET /v1/subscription_items/{item}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `subscription_item`
  - Filters:
    - `item` eq `path.item`
  - Notes:
    - Response body references #/components/schemas/subscription_item
    - Query parameters: expand

#### `POST /v1/subscription_items`
**Status:** planned

**Operations:**
- **create**
  - Component: `subscription_item`
  - Notes:
    - Response body references #/components/schemas/subscription_item

#### `POST /v1/subscription_items/{item}`
**Status:** planned

**Operations:**
- **create**
  - Component: `subscription_item`
  - Filters:
    - `item` eq `path.item`
  - Notes:
    - Response body references #/components/schemas/subscription_item
    - Query parameters: item

### Component: `subscription_schedule`

#### `GET /v1/subscription_schedules/{schedule}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `subscription_schedule`
  - Filters:
    - `schedule` eq `path.schedule`
  - Notes:
    - Response body references #/components/schemas/subscription_schedule
    - Query parameters: expand

#### `POST /v1/subscription_schedules`
**Status:** planned

**Operations:**
- **create**
  - Component: `subscription_schedule`
  - Notes:
    - Response body references #/components/schemas/subscription_schedule

#### `POST /v1/subscription_schedules/{schedule}`
**Status:** planned

**Operations:**
- **create**
  - Component: `subscription_schedule`
  - Filters:
    - `schedule` eq `path.schedule`
  - Notes:
    - Response body references #/components/schemas/subscription_schedule
    - Query parameters: schedule

#### `POST /v1/subscription_schedules/{schedule}/cancel`
**Status:** planned

**Operations:**
- **create**
  - Component: `subscription_schedule`
  - Filters:
    - `schedule` eq `path.schedule`
  - Notes:
    - Response body references #/components/schemas/subscription_schedule
    - Query parameters: schedule

#### `POST /v1/subscription_schedules/{schedule}/release`
**Status:** planned

**Operations:**
- **create**
  - Component: `subscription_schedule`
  - Filters:
    - `schedule` eq `path.schedule`
  - Notes:
    - Response body references #/components/schemas/subscription_schedule
    - Query parameters: schedule

### Component: `tax.calculation`

#### `GET /v1/tax/calculations/{calculation}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `tax.calculation`
  - Filters:
    - `calculation` eq `path.calculation`
  - Notes:
    - Response body references #/components/schemas/tax.calculation
    - Query parameters: expand

#### `POST /v1/tax/calculations`
**Status:** planned

**Operations:**
- **create**
  - Component: `tax.calculation`
  - Notes:
    - Response body references #/components/schemas/tax.calculation

### Component: `tax.registration`

#### `GET /v1/tax/registrations/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `tax.registration`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/tax.registration
    - Query parameters: expand

#### `POST /v1/tax/registrations`
**Status:** planned

**Operations:**
- **create**
  - Component: `tax.registration`
  - Notes:
    - Response body references #/components/schemas/tax.registration

#### `POST /v1/tax/registrations/{id}`
**Status:** planned

**Operations:**
- **create**
  - Component: `tax.registration`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/tax.registration
    - Query parameters: id

### Component: `tax.settings`

#### `GET /v1/tax/settings`
**Status:** planned

**Operations:**
- **read_many**
  - Component: `tax.settings`
  - Notes:
    - Response body references #/components/schemas/tax.settings
    - Query parameters: expand

#### `POST /v1/tax/settings`
**Status:** planned

**Operations:**
- **create**
  - Component: `tax.settings`
  - Notes:
    - Response body references #/components/schemas/tax.settings

### Component: `tax.transaction`

#### `GET /v1/tax/transactions/{transaction}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `tax.transaction`
  - Filters:
    - `transaction` eq `path.transaction`
  - Notes:
    - Response body references #/components/schemas/tax.transaction
    - Query parameters: expand

#### `POST /v1/tax/transactions/create_from_calculation`
**Status:** planned

**Operations:**
- **create**
  - Component: `tax.transaction`
  - Notes:
    - Response body references #/components/schemas/tax.transaction

#### `POST /v1/tax/transactions/create_reversal`
**Status:** planned

**Operations:**
- **create**
  - Component: `tax.transaction`
  - Notes:
    - Response body references #/components/schemas/tax.transaction

### Component: `tax_code`

#### `GET /v1/tax_codes/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `tax_code`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/tax_code
    - Query parameters: expand

### Component: `tax_id`

#### `GET /v1/customers/{customer}/tax_ids/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `tax_id`
  - Filters:
    - `customer` eq `path.customer`
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/tax_id
    - Query parameters: expand

#### `GET /v1/tax_ids/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `tax_id`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/tax_id
    - Query parameters: expand

#### `POST /v1/customers/{customer}/tax_ids`
**Status:** planned

**Operations:**
- **create**
  - Component: `tax_id`
  - Filters:
    - `customer` eq `path.customer`
  - Notes:
    - Response body references #/components/schemas/tax_id
    - Query parameters: customer

#### `POST /v1/tax_ids`
**Status:** planned

**Operations:**
- **create**
  - Component: `tax_id`
  - Notes:
    - Response body references #/components/schemas/tax_id

### Component: `tax_rate`

#### `GET /v1/tax_rates/{tax_rate}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `tax_rate`
  - Filters:
    - `tax_rate` eq `path.tax_rate`
  - Notes:
    - Response body references #/components/schemas/tax_rate
    - Query parameters: expand

#### `POST /v1/tax_rates`
**Status:** planned

**Operations:**
- **create**
  - Component: `tax_rate`
  - Notes:
    - Response body references #/components/schemas/tax_rate

#### `POST /v1/tax_rates/{tax_rate}`
**Status:** planned

**Operations:**
- **create**
  - Component: `tax_rate`
  - Filters:
    - `tax_rate` eq `path.tax_rate`
  - Notes:
    - Response body references #/components/schemas/tax_rate
    - Query parameters: tax_rate

### Component: `terminal.configuration`

#### `POST /v1/terminal/configurations`
**Status:** planned

**Operations:**
- **create**
  - Component: `terminal.configuration`
  - Notes:
    - Response body references #/components/schemas/terminal.configuration

### Component: `terminal.connection_token`

#### `POST /v1/terminal/connection_tokens`
**Status:** planned

**Operations:**
- **create**
  - Component: `terminal.connection_token`
  - Notes:
    - Response body references #/components/schemas/terminal.connection_token

### Component: `terminal.location`

#### `POST /v1/terminal/locations`
**Status:** planned

**Operations:**
- **create**
  - Component: `terminal.location`
  - Notes:
    - Response body references #/components/schemas/terminal.location

### Component: `terminal.reader`

#### `POST /v1/terminal/readers`
**Status:** planned

**Operations:**
- **create**
  - Component: `terminal.reader`
  - Notes:
    - Response body references #/components/schemas/terminal.reader

#### `POST /v1/terminal/readers/{reader}/cancel_action`
**Status:** planned

**Operations:**
- **create**
  - Component: `terminal.reader`
  - Filters:
    - `reader` eq `path.reader`
  - Notes:
    - Response body references #/components/schemas/terminal.reader
    - Query parameters: reader

#### `POST /v1/terminal/readers/{reader}/process_payment_intent`
**Status:** planned

**Operations:**
- **create**
  - Component: `terminal.reader`
  - Filters:
    - `reader` eq `path.reader`
  - Notes:
    - Response body references #/components/schemas/terminal.reader
    - Query parameters: reader

#### `POST /v1/terminal/readers/{reader}/process_setup_intent`
**Status:** planned

**Operations:**
- **create**
  - Component: `terminal.reader`
  - Filters:
    - `reader` eq `path.reader`
  - Notes:
    - Response body references #/components/schemas/terminal.reader
    - Query parameters: reader

#### `POST /v1/terminal/readers/{reader}/refund_payment`
**Status:** planned

**Operations:**
- **create**
  - Component: `terminal.reader`
  - Filters:
    - `reader` eq `path.reader`
  - Notes:
    - Response body references #/components/schemas/terminal.reader
    - Query parameters: reader

#### `POST /v1/terminal/readers/{reader}/set_reader_display`
**Status:** planned

**Operations:**
- **create**
  - Component: `terminal.reader`
  - Filters:
    - `reader` eq `path.reader`
  - Notes:
    - Response body references #/components/schemas/terminal.reader
    - Query parameters: reader

#### `POST /v1/test_helpers/terminal/readers/{reader}/present_payment_method`
**Status:** planned

**Operations:**
- **create**
  - Component: `terminal.reader`
  - Filters:
    - `reader` eq `path.reader`
  - Notes:
    - Response body references #/components/schemas/terminal.reader
    - Query parameters: reader

### Component: `test_helpers.test_clock`

#### `GET /v1/test_helpers/test_clocks/{test_clock}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `test_helpers.test_clock`
  - Filters:
    - `test_clock` eq `path.test_clock`
  - Notes:
    - Response body references #/components/schemas/test_helpers.test_clock
    - Query parameters: expand

#### `POST /v1/test_helpers/test_clocks`
**Status:** planned

**Operations:**
- **create**
  - Component: `test_helpers.test_clock`
  - Notes:
    - Response body references #/components/schemas/test_helpers.test_clock

#### `POST /v1/test_helpers/test_clocks/{test_clock}/advance`
**Status:** planned

**Operations:**
- **create**
  - Component: `test_helpers.test_clock`
  - Filters:
    - `test_clock` eq `path.test_clock`
  - Notes:
    - Response body references #/components/schemas/test_helpers.test_clock
    - Query parameters: test_clock

### Component: `token`

#### `GET /v1/tokens/{token}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `token`
  - Filters:
    - `token` eq `path.token`
  - Notes:
    - Response body references #/components/schemas/token
    - Query parameters: expand

#### `POST /v1/tokens`
**Status:** planned

**Operations:**
- **create**
  - Component: `token`
  - Notes:
    - Response body references #/components/schemas/token

### Component: `topup`

#### `GET /v1/topups/{topup}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `topup`
  - Filters:
    - `topup` eq `path.topup`
  - Notes:
    - Response body references #/components/schemas/topup
    - Query parameters: expand

#### `POST /v1/topups`
**Status:** planned

**Operations:**
- **create**
  - Component: `topup`
  - Notes:
    - Response body references #/components/schemas/topup

#### `POST /v1/topups/{topup}`
**Status:** planned

**Operations:**
- **create**
  - Component: `topup`
  - Filters:
    - `topup` eq `path.topup`
  - Notes:
    - Response body references #/components/schemas/topup
    - Query parameters: topup

#### `POST /v1/topups/{topup}/cancel`
**Status:** planned

**Operations:**
- **create**
  - Component: `topup`
  - Filters:
    - `topup` eq `path.topup`
  - Notes:
    - Response body references #/components/schemas/topup
    - Query parameters: topup

### Component: `transfer`

#### `GET /v1/transfers/{transfer}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `transfer`
  - Filters:
    - `transfer_group` eq `path.transfer`
  - Notes:
    - Response body references #/components/schemas/transfer
    - Query parameters: expand

#### `POST /v1/transfers`
**Status:** planned

**Operations:**
- **create**
  - Component: `transfer`
  - Notes:
    - Response body references #/components/schemas/transfer

#### `POST /v1/transfers/{transfer}`
**Status:** planned

**Operations:**
- **create**
  - Component: `transfer`
  - Filters:
    - `transfer_group` eq `path.transfer`
  - Notes:
    - Response body references #/components/schemas/transfer
    - Query parameters: transfer

### Component: `transfer_reversal`

#### `GET /v1/transfers/{transfer}/reversals/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `transfer_reversal`
  - Filters:
    - `id` eq `path.id`
    - `transfer` eq `path.transfer`
  - Notes:
    - Response body references #/components/schemas/transfer_reversal
    - Query parameters: expand

#### `POST /v1/transfers/{id}/reversals`
**Status:** planned

**Operations:**
- **create**
  - Component: `transfer_reversal`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/transfer_reversal
    - Query parameters: id

#### `POST /v1/transfers/{transfer}/reversals/{id}`
**Status:** planned

**Operations:**
- **create**
  - Component: `transfer_reversal`
  - Filters:
    - `id` eq `path.id`
    - `transfer` eq `path.transfer`
  - Notes:
    - Response body references #/components/schemas/transfer_reversal
    - Query parameters: id, transfer

### Component: `treasury.credit_reversal`

#### `GET /v1/treasury/credit_reversals/{credit_reversal}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `treasury.credit_reversal`
  - Filters:
    - `credit_reversal` eq `path.credit_reversal`
  - Notes:
    - Response body references #/components/schemas/treasury.credit_reversal
    - Query parameters: expand

#### `POST /v1/treasury/credit_reversals`
**Status:** planned

**Operations:**
- **create**
  - Component: `treasury.credit_reversal`
  - Notes:
    - Response body references #/components/schemas/treasury.credit_reversal

### Component: `treasury.debit_reversal`

#### `GET /v1/treasury/debit_reversals/{debit_reversal}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `treasury.debit_reversal`
  - Filters:
    - `debit_reversal` eq `path.debit_reversal`
  - Notes:
    - Response body references #/components/schemas/treasury.debit_reversal
    - Query parameters: expand

#### `POST /v1/treasury/debit_reversals`
**Status:** planned

**Operations:**
- **create**
  - Component: `treasury.debit_reversal`
  - Notes:
    - Response body references #/components/schemas/treasury.debit_reversal

### Component: `treasury.financial_account`

#### `GET /v1/treasury/financial_accounts/{financial_account}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `treasury.financial_account`
  - Filters:
    - `financial_account` eq `path.financial_account`
  - Notes:
    - Response body references #/components/schemas/treasury.financial_account
    - Query parameters: expand

#### `POST /v1/treasury/financial_accounts`
**Status:** planned

**Operations:**
- **create**
  - Component: `treasury.financial_account`
  - Notes:
    - Response body references #/components/schemas/treasury.financial_account

#### `POST /v1/treasury/financial_accounts/{financial_account}`
**Status:** planned

**Operations:**
- **create**
  - Component: `treasury.financial_account`
  - Filters:
    - `financial_account` eq `path.financial_account`
  - Notes:
    - Response body references #/components/schemas/treasury.financial_account
    - Query parameters: financial_account

### Component: `treasury.financial_account_features`

#### `GET /v1/treasury/financial_accounts/{financial_account}/features`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `treasury.financial_account_features`
  - Filters:
    - `financial_account` eq `path.financial_account`
  - Notes:
    - Response body references #/components/schemas/treasury.financial_account_features
    - Query parameters: expand

#### `POST /v1/treasury/financial_accounts/{financial_account}/features`
**Status:** planned

**Operations:**
- **create**
  - Component: `treasury.financial_account_features`
  - Filters:
    - `financial_account` eq `path.financial_account`
  - Notes:
    - Response body references #/components/schemas/treasury.financial_account_features
    - Query parameters: financial_account

### Component: `treasury.inbound_transfer`

#### `GET /v1/treasury/inbound_transfers/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `treasury.inbound_transfer`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/treasury.inbound_transfer
    - Query parameters: expand

#### `POST /v1/test_helpers/treasury/inbound_transfers/{id}/fail`
**Status:** planned

**Operations:**
- **create**
  - Component: `treasury.inbound_transfer`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/treasury.inbound_transfer
    - Query parameters: id

#### `POST /v1/test_helpers/treasury/inbound_transfers/{id}/return`
**Status:** planned

**Operations:**
- **create**
  - Component: `treasury.inbound_transfer`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/treasury.inbound_transfer
    - Query parameters: id

#### `POST /v1/test_helpers/treasury/inbound_transfers/{id}/succeed`
**Status:** planned

**Operations:**
- **create**
  - Component: `treasury.inbound_transfer`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/treasury.inbound_transfer
    - Query parameters: id

#### `POST /v1/treasury/inbound_transfers`
**Status:** planned

**Operations:**
- **create**
  - Component: `treasury.inbound_transfer`
  - Notes:
    - Response body references #/components/schemas/treasury.inbound_transfer

#### `POST /v1/treasury/inbound_transfers/{inbound_transfer}/cancel`
**Status:** planned

**Operations:**
- **create**
  - Component: `treasury.inbound_transfer`
  - Filters:
    - `inbound_transfer` eq `path.inbound_transfer`
  - Notes:
    - Response body references #/components/schemas/treasury.inbound_transfer
    - Query parameters: inbound_transfer

### Component: `treasury.outbound_payment`

#### `GET /v1/treasury/outbound_payments/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `treasury.outbound_payment`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/treasury.outbound_payment
    - Query parameters: expand

#### `POST /v1/test_helpers/treasury/outbound_payments/{id}`
**Status:** planned

**Operations:**
- **create**
  - Component: `treasury.outbound_payment`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/treasury.outbound_payment
    - Query parameters: id

#### `POST /v1/test_helpers/treasury/outbound_payments/{id}/fail`
**Status:** planned

**Operations:**
- **create**
  - Component: `treasury.outbound_payment`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/treasury.outbound_payment
    - Query parameters: id

#### `POST /v1/test_helpers/treasury/outbound_payments/{id}/post`
**Status:** planned

**Operations:**
- **create**
  - Component: `treasury.outbound_payment`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/treasury.outbound_payment
    - Query parameters: id

#### `POST /v1/test_helpers/treasury/outbound_payments/{id}/return`
**Status:** planned

**Operations:**
- **create**
  - Component: `treasury.outbound_payment`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/treasury.outbound_payment
    - Query parameters: id

#### `POST /v1/treasury/outbound_payments`
**Status:** planned

**Operations:**
- **create**
  - Component: `treasury.outbound_payment`
  - Notes:
    - Response body references #/components/schemas/treasury.outbound_payment

#### `POST /v1/treasury/outbound_payments/{id}/cancel`
**Status:** planned

**Operations:**
- **create**
  - Component: `treasury.outbound_payment`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/treasury.outbound_payment
    - Query parameters: id

### Component: `treasury.outbound_transfer`

#### `GET /v1/treasury/outbound_transfers/{outbound_transfer}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `treasury.outbound_transfer`
  - Filters:
    - `outbound_transfer` eq `path.outbound_transfer`
  - Notes:
    - Response body references #/components/schemas/treasury.outbound_transfer
    - Query parameters: expand

#### `POST /v1/test_helpers/treasury/outbound_transfers/{outbound_transfer}`
**Status:** planned

**Operations:**
- **create**
  - Component: `treasury.outbound_transfer`
  - Filters:
    - `outbound_transfer` eq `path.outbound_transfer`
  - Notes:
    - Response body references #/components/schemas/treasury.outbound_transfer
    - Query parameters: outbound_transfer

#### `POST /v1/test_helpers/treasury/outbound_transfers/{outbound_transfer}/fail`
**Status:** planned

**Operations:**
- **create**
  - Component: `treasury.outbound_transfer`
  - Filters:
    - `outbound_transfer` eq `path.outbound_transfer`
  - Notes:
    - Response body references #/components/schemas/treasury.outbound_transfer
    - Query parameters: outbound_transfer

#### `POST /v1/test_helpers/treasury/outbound_transfers/{outbound_transfer}/post`
**Status:** planned

**Operations:**
- **create**
  - Component: `treasury.outbound_transfer`
  - Filters:
    - `outbound_transfer` eq `path.outbound_transfer`
  - Notes:
    - Response body references #/components/schemas/treasury.outbound_transfer
    - Query parameters: outbound_transfer

#### `POST /v1/test_helpers/treasury/outbound_transfers/{outbound_transfer}/return`
**Status:** planned

**Operations:**
- **create**
  - Component: `treasury.outbound_transfer`
  - Filters:
    - `outbound_transfer` eq `path.outbound_transfer`
  - Notes:
    - Response body references #/components/schemas/treasury.outbound_transfer
    - Query parameters: outbound_transfer

#### `POST /v1/treasury/outbound_transfers`
**Status:** planned

**Operations:**
- **create**
  - Component: `treasury.outbound_transfer`
  - Notes:
    - Response body references #/components/schemas/treasury.outbound_transfer

#### `POST /v1/treasury/outbound_transfers/{outbound_transfer}/cancel`
**Status:** planned

**Operations:**
- **create**
  - Component: `treasury.outbound_transfer`
  - Filters:
    - `outbound_transfer` eq `path.outbound_transfer`
  - Notes:
    - Response body references #/components/schemas/treasury.outbound_transfer
    - Query parameters: outbound_transfer

### Component: `treasury.received_credit`

#### `GET /v1/treasury/received_credits/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `treasury.received_credit`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/treasury.received_credit
    - Query parameters: expand

#### `POST /v1/test_helpers/treasury/received_credits`
**Status:** planned

**Operations:**
- **create**
  - Component: `treasury.received_credit`
  - Notes:
    - Response body references #/components/schemas/treasury.received_credit

### Component: `treasury.received_debit`

#### `GET /v1/treasury/received_debits/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `treasury.received_debit`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/treasury.received_debit
    - Query parameters: expand

#### `POST /v1/test_helpers/treasury/received_debits`
**Status:** planned

**Operations:**
- **create**
  - Component: `treasury.received_debit`
  - Notes:
    - Response body references #/components/schemas/treasury.received_debit

### Component: `treasury.transaction`

#### `GET /v1/treasury/transactions/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `treasury.transaction`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/treasury.transaction
    - Query parameters: expand

### Component: `treasury.transaction_entry`

#### `GET /v1/treasury/transaction_entries/{id}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `treasury.transaction_entry`
  - Filters:
    - `id` eq `path.id`
  - Notes:
    - Response body references #/components/schemas/treasury.transaction_entry
    - Query parameters: expand

### Component: `usage_record`

#### `POST /v1/subscription_items/{subscription_item}/usage_records`
**Status:** planned

**Operations:**
- **create**
  - Component: `usage_record`
  - Filters:
    - `subscription_item` eq `path.subscription_item`
  - Notes:
    - Response body references #/components/schemas/usage_record
    - Query parameters: subscription_item

### Component: `webhook_endpoint`

#### `GET /v1/webhook_endpoints/{webhook_endpoint}`
**Status:** planned

**Operations:**
- **read_one**
  - Component: `webhook_endpoint`
  - Filters:
    - `webhook_endpoint` eq `path.webhook_endpoint`
  - Notes:
    - Response body references #/components/schemas/webhook_endpoint
    - Query parameters: expand

#### `POST /v1/webhook_endpoints`
**Status:** planned

**Operations:**
- **create**
  - Component: `webhook_endpoint`
  - Notes:
    - Response body references #/components/schemas/webhook_endpoint

#### `POST /v1/webhook_endpoints/{webhook_endpoint}`
**Status:** planned

**Operations:**
- **create**
  - Component: `webhook_endpoint`
  - Filters:
    - `webhook_endpoint` eq `path.webhook_endpoint`
  - Notes:
    - Response body references #/components/schemas/webhook_endpoint
    - Query parameters: webhook_endpoint

## Route Summary

| Method | Path | Component | Status | Operations |
|--------|------|-----------|--------|------------|
| DELETE | `/v1/accounts/{account}` | deleted_account | planned | delete |
| DELETE | `/v1/accounts/{account}/bank_accounts/{id}` | deleted_external_account | planned | delete |
| DELETE | `/v1/accounts/{account}/external_accounts/{id}` | deleted_external_account | planned | delete |
| DELETE | `/v1/accounts/{account}/people/{person}` | deleted_person | planned | delete |
| DELETE | `/v1/accounts/{account}/persons/{person}` | deleted_person | planned | delete |
| DELETE | `/v1/apple_pay/domains/{domain}` | deleted_apple_pay_domain | planned | delete |
| DELETE | `/v1/coupons/{coupon}` | deleted_coupon | planned | delete |
| DELETE | `/v1/customers/{customer}` | deleted_customer | planned | delete |
| DELETE | `/v1/customers/{customer}/bank_accounts/{id}` | error | planned | delete |
| DELETE | `/v1/customers/{customer}/cards/{id}` | error | planned | delete |
| DELETE | `/v1/customers/{customer}/discount` | deleted_discount | planned | delete |
| DELETE | `/v1/customers/{customer}/sources/{id}` | error | planned | delete |
| DELETE | `/v1/customers/{customer}/subscriptions/{subscription_exposed_id}` | subscription | planned | delete |
| DELETE | `/v1/customers/{customer}/subscriptions/{subscription_exposed_id}/discount` | deleted_discount | planned | delete |
| DELETE | `/v1/customers/{customer}/tax_ids/{id}` | deleted_tax_id | planned | delete |
| DELETE | `/v1/ephemeral_keys/{key}` | ephemeral_key | planned | delete |
| DELETE | `/v1/invoiceitems/{invoiceitem}` | deleted_invoiceitem | planned | delete |
| DELETE | `/v1/invoices/{invoice}` | deleted_invoice | planned | delete |
| DELETE | `/v1/plans/{plan}` | deleted_plan | planned | delete |
| DELETE | `/v1/products/{id}` | deleted_product | planned | delete |
| DELETE | `/v1/products/{product}/features/{id}` | deleted_product_feature | planned | delete |
| DELETE | `/v1/radar/value_list_items/{item}` | deleted_radar.value_list_item | planned | delete |
| DELETE | `/v1/radar/value_lists/{value_list}` | deleted_radar.value_list | planned | delete |
| DELETE | `/v1/subscription_items/{item}` | deleted_subscription_item | planned | delete |
| DELETE | `/v1/subscriptions/{subscription_exposed_id}` | subscription | planned | delete |
| DELETE | `/v1/subscriptions/{subscription_exposed_id}/discount` | deleted_discount | planned | delete |
| DELETE | `/v1/tax_ids/{id}` | deleted_tax_id | planned | delete |
| DELETE | `/v1/terminal/configurations/{configuration}` | deleted_terminal.configuration | planned | delete |
| DELETE | `/v1/terminal/locations/{location}` | deleted_terminal.location | planned | delete |
| DELETE | `/v1/terminal/readers/{reader}` | deleted_terminal.reader | planned | delete |
| DELETE | `/v1/test_helpers/test_clocks/{test_clock}` | deleted_test_helpers.test_clock | planned | delete |
| DELETE | `/v1/webhook_endpoints/{webhook_endpoint}` | deleted_webhook_endpoint | planned | delete |
| GET | `/v1/account` | account | planned | read_many |
| GET | `/v1/accounts` | error | planned | read_many |
| GET | `/v1/accounts/{account}` | account | planned | read_one |
| GET | `/v1/accounts/{account}/bank_accounts/{id}` | external_account | planned | read_one |
| GET | `/v1/accounts/{account}/capabilities` | error | planned | read_one |
| GET | `/v1/accounts/{account}/capabilities/{capability}` | capability | planned | read_one |
| GET | `/v1/accounts/{account}/external_accounts` | error | planned | read_one |
| GET | `/v1/accounts/{account}/external_accounts/{id}` | external_account | planned | read_one |
| GET | `/v1/accounts/{account}/people` | error | planned | read_one |
| GET | `/v1/accounts/{account}/people/{person}` | person | planned | read_one |
| GET | `/v1/accounts/{account}/persons` | error | planned | read_one |
| GET | `/v1/accounts/{account}/persons/{person}` | person | planned | read_one |
| GET | `/v1/apple_pay/domains` | error | planned | read_many |
| GET | `/v1/apple_pay/domains/{domain}` | apple_pay_domain | planned | read_one |
| GET | `/v1/application_fees` | error | planned | read_many |
| GET | `/v1/application_fees/{fee}/refunds/{id}` | fee_refund | planned | read_one |
| GET | `/v1/application_fees/{id}` | application_fee | planned | read_one |
| GET | `/v1/application_fees/{id}/refunds` | error | planned | read_one |
| GET | `/v1/apps/secrets` | error | planned | read_many |
| GET | `/v1/apps/secrets/find` | apps.secret | planned | read_many |
| GET | `/v1/balance` | balance | planned | read_many |
| GET | `/v1/balance/history` | error | planned | read_many |
| GET | `/v1/balance/history/{id}` | balance_transaction | planned | read_one |
| GET | `/v1/balance_transactions` | error | planned | read_many |
| GET | `/v1/balance_transactions/{id}` | balance_transaction | planned | read_one |
| GET | `/v1/billing/alerts` | error | planned | read_many |
| GET | `/v1/billing/alerts/{id}` | billing.alert | planned | read_one |
| GET | `/v1/billing/credit_balance_summary` | billing.credit_balance_summary | planned | read_many |
| GET | `/v1/billing/credit_balance_transactions` | error | planned | read_many |
| GET | `/v1/billing/credit_balance_transactions/{id}` | billing.credit_balance_transaction | planned | read_one |
| GET | `/v1/billing/credit_grants` | error | planned | read_many |
| GET | `/v1/billing/credit_grants/{id}` | billing.credit_grant | planned | read_one |
| GET | `/v1/billing/meters` | error | planned | read_many |
| GET | `/v1/billing/meters/{id}` | billing.meter | planned | read_one |
| GET | `/v1/billing/meters/{id}/event_summaries` | error | planned | read_one |
| GET | `/v1/billing_portal/configurations` | error | planned | read_many |
| GET | `/v1/billing_portal/configurations/{configuration}` | billing_portal.configuration | planned | read_one |
| GET | `/v1/charges` | error | planned | read_many |
| GET | `/v1/charges/search` | error | planned | read_many |
| GET | `/v1/charges/{charge}` | charge | planned | read_one |
| GET | `/v1/charges/{charge}/dispute` | dispute | planned | read_one |
| GET | `/v1/charges/{charge}/refunds` | error | planned | read_one |
| GET | `/v1/charges/{charge}/refunds/{refund}` | refund | planned | read_one |
| GET | `/v1/checkout/sessions` | error | planned | read_many |
| GET | `/v1/checkout/sessions/{session}` | checkout.session | planned | read_one |
| GET | `/v1/checkout/sessions/{session}/line_items` | error | planned | read_one |
| GET | `/v1/climate/orders` | error | planned | read_many |
| GET | `/v1/climate/orders/{order}` | climate.order | planned | read_one |
| GET | `/v1/climate/products` | error | planned | read_many |
| GET | `/v1/climate/products/{product}` | climate.product | planned | read_one |
| GET | `/v1/climate/suppliers` | error | planned | read_many |
| GET | `/v1/climate/suppliers/{supplier}` | climate.supplier | planned | read_one |
| GET | `/v1/confirmation_tokens/{confirmation_token}` | confirmation_token | planned | read_one |
| GET | `/v1/country_specs` | error | planned | read_many |
| GET | `/v1/country_specs/{country}` | country_spec | planned | read_one |
| GET | `/v1/coupons` | error | planned | read_many |
| GET | `/v1/coupons/{coupon}` | coupon | planned | read_one |
| GET | `/v1/credit_notes` | error | planned | read_many |
| GET | `/v1/credit_notes/preview` | credit_note | planned | read_many |
| GET | `/v1/credit_notes/preview/lines` | error | planned | read_many |
| GET | `/v1/credit_notes/{credit_note}/lines` | error | planned | read_one |
| GET | `/v1/credit_notes/{id}` | credit_note | planned | read_one |
| GET | `/v1/customers` | error | planned | read_many |
| GET | `/v1/customers/search` | error | planned | read_many |
| GET | `/v1/customers/{customer}` | error | planned | read_one |
| GET | `/v1/customers/{customer}/balance_transactions` | error | planned | read_one |
| GET | `/v1/customers/{customer}/balance_transactions/{transaction}` | customer_balance_transaction | planned | read_one |
| GET | `/v1/customers/{customer}/bank_accounts` | error | planned | read_one |
| GET | `/v1/customers/{customer}/bank_accounts/{id}` | bank_account | planned | read_one |
| GET | `/v1/customers/{customer}/cards` | error | planned | read_one |
| GET | `/v1/customers/{customer}/cards/{id}` | card | planned | read_one |
| GET | `/v1/customers/{customer}/cash_balance` | cash_balance | planned | read_one |
| GET | `/v1/customers/{customer}/cash_balance_transactions` | error | planned | read_one |
| GET | `/v1/customers/{customer}/cash_balance_transactions/{transaction}` | customer_cash_balance_transaction | planned | read_one |
| GET | `/v1/customers/{customer}/discount` | discount | planned | read_one |
| GET | `/v1/customers/{customer}/payment_methods` | error | planned | read_one |
| GET | `/v1/customers/{customer}/payment_methods/{payment_method}` | payment_method | planned | read_one |
| GET | `/v1/customers/{customer}/sources` | error | planned | read_one |
| GET | `/v1/customers/{customer}/sources/{id}` | payment_source | planned | read_one |
| GET | `/v1/customers/{customer}/subscriptions` | error | planned | read_one |
| GET | `/v1/customers/{customer}/subscriptions/{subscription_exposed_id}` | subscription | planned | read_one |
| GET | `/v1/customers/{customer}/subscriptions/{subscription_exposed_id}/discount` | discount | planned | read_one |
| GET | `/v1/customers/{customer}/tax_ids` | error | planned | read_one |
| GET | `/v1/customers/{customer}/tax_ids/{id}` | tax_id | planned | read_one |
| GET | `/v1/disputes` | error | planned | read_many |
| GET | `/v1/disputes/{dispute}` | dispute | planned | read_one |
| GET | `/v1/entitlements/active_entitlements` | error | planned | read_many |
| GET | `/v1/entitlements/active_entitlements/{id}` | entitlements.active_entitlement | planned | read_one |
| GET | `/v1/entitlements/features` | error | planned | read_many |
| GET | `/v1/entitlements/features/{id}` | entitlements.feature | planned | read_one |
| GET | `/v1/events` | error | planned | read_many |
| GET | `/v1/events/{id}` | event | planned | read_one |
| GET | `/v1/exchange_rates` | error | planned | read_many |
| GET | `/v1/exchange_rates/{rate_id}` | exchange_rate | planned | read_one |
| GET | `/v1/file_links` | error | planned | read_many |
| GET | `/v1/file_links/{link}` | file_link | planned | read_one |
| GET | `/v1/files` | error | planned | read_many |
| GET | `/v1/files/{file}` | file | planned | read_one |
| GET | `/v1/financial_connections/accounts` | error | planned | read_many |
| GET | `/v1/financial_connections/accounts/{account}` | financial_connections.account | planned | read_one |
| GET | `/v1/financial_connections/accounts/{account}/owners` | error | planned | read_one |
| GET | `/v1/financial_connections/sessions/{session}` | financial_connections.session | planned | read_one |
| GET | `/v1/financial_connections/transactions` | error | planned | read_many |
| GET | `/v1/financial_connections/transactions/{transaction}` | financial_connections.transaction | planned | read_one |
| GET | `/v1/forwarding/requests` | error | planned | read_many |
| GET | `/v1/forwarding/requests/{id}` | forwarding.request | planned | read_one |
| GET | `/v1/identity/verification_reports` | error | planned | read_many |
| GET | `/v1/identity/verification_reports/{report}` | identity.verification_report | planned | read_one |
| GET | `/v1/identity/verification_sessions` | error | planned | read_many |
| GET | `/v1/identity/verification_sessions/{session}` | identity.verification_session | planned | read_one |
| GET | `/v1/invoice_rendering_templates` | error | planned | read_many |
| GET | `/v1/invoice_rendering_templates/{template}` | invoice_rendering_template | planned | read_one |
| GET | `/v1/invoiceitems` | error | planned | read_many |
| GET | `/v1/invoiceitems/{invoiceitem}` | invoiceitem | planned | read_one |
| GET | `/v1/invoices` | error | planned | read_many |
| GET | `/v1/invoices/search` | error | planned | read_many |
| GET | `/v1/invoices/upcoming` | invoice | planned | read_many |
| GET | `/v1/invoices/upcoming/lines` | error | planned | read_many |
| GET | `/v1/invoices/{invoice}` | invoice | planned | read_one |
| GET | `/v1/invoices/{invoice}/lines` | error | planned | read_one |
| GET | `/v1/issuing/authorizations` | error | planned | read_many |
| GET | `/v1/issuing/authorizations/{authorization}` | issuing.authorization | planned | read_one |
| GET | `/v1/issuing/cardholders` | error | planned | read_many |
| GET | `/v1/issuing/cardholders/{cardholder}` | issuing.cardholder | planned | read_one |
| GET | `/v1/issuing/cards` | error | planned | read_many |
| GET | `/v1/issuing/cards/{card}` | issuing.card | planned | read_one |
| GET | `/v1/issuing/disputes` | error | planned | read_many |
| GET | `/v1/issuing/disputes/{dispute}` | issuing.dispute | planned | read_one |
| GET | `/v1/issuing/personalization_designs` | error | planned | read_many |
| GET | `/v1/issuing/personalization_designs/{personalization_design}` | issuing.personalization_design | planned | read_one |
| GET | `/v1/issuing/physical_bundles` | error | planned | read_many |
| GET | `/v1/issuing/physical_bundles/{physical_bundle}` | issuing.physical_bundle | planned | read_one |
| GET | `/v1/issuing/settlements/{settlement}` | issuing.settlement | planned | read_one |
| GET | `/v1/issuing/tokens` | error | planned | read_many |
| GET | `/v1/issuing/tokens/{token}` | issuing.token | planned | read_one |
| GET | `/v1/issuing/transactions` | error | planned | read_many |
| GET | `/v1/issuing/transactions/{transaction}` | issuing.transaction | planned | read_one |
| GET | `/v1/link_account_sessions/{session}` | financial_connections.session | planned | read_one |
| GET | `/v1/linked_accounts` | error | planned | read_many |
| GET | `/v1/linked_accounts/{account}` | financial_connections.account | planned | read_one |
| GET | `/v1/linked_accounts/{account}/owners` | error | planned | read_one |
| GET | `/v1/mandates/{mandate}` | mandate | planned | read_one |
| GET | `/v1/payment_intents` | error | planned | read_many |
| GET | `/v1/payment_intents/search` | error | planned | read_many |
| GET | `/v1/payment_intents/{intent}` | payment_intent | planned | read_one |
| GET | `/v1/payment_links` | error | planned | read_many |
| GET | `/v1/payment_links/{payment_link}` | payment_link | planned | read_one |
| GET | `/v1/payment_links/{payment_link}/line_items` | error | planned | read_one |
| GET | `/v1/payment_method_configurations` | error | planned | read_many |
| GET | `/v1/payment_method_configurations/{configuration}` | payment_method_configuration | planned | read_one |
| GET | `/v1/payment_method_domains` | error | planned | read_many |
| GET | `/v1/payment_method_domains/{payment_method_domain}` | payment_method_domain | planned | read_one |
| GET | `/v1/payment_methods` | error | planned | read_many |
| GET | `/v1/payment_methods/{payment_method}` | payment_method | planned | read_one |
| GET | `/v1/payouts` | error | planned | read_many |
| GET | `/v1/payouts/{payout}` | payout | planned | read_one |
| GET | `/v1/plans` | error | planned | read_many |
| GET | `/v1/plans/{plan}` | plan | planned | read_one |
| GET | `/v1/prices` | error | planned | read_many |
| GET | `/v1/prices/search` | error | planned | read_many |
| GET | `/v1/prices/{price}` | price | planned | read_one |
| GET | `/v1/products` | error | planned | read_many |
| GET | `/v1/products/search` | error | planned | read_many |
| GET | `/v1/products/{id}` | product | planned | read_one |
| GET | `/v1/products/{product}/features` | error | planned | read_one |
| GET | `/v1/products/{product}/features/{id}` | product_feature | planned | read_one |
| GET | `/v1/promotion_codes` | error | planned | read_many |
| GET | `/v1/promotion_codes/{promotion_code}` | promotion_code | planned | read_one |
| GET | `/v1/quotes` | error | planned | read_many |
| GET | `/v1/quotes/{quote}` | quote | planned | read_one |
| GET | `/v1/quotes/{quote}/computed_upfront_line_items` | error | planned | read_one |
| GET | `/v1/quotes/{quote}/line_items` | error | planned | read_one |
| GET | `/v1/quotes/{quote}/pdf` | error | planned | read_one |
| GET | `/v1/radar/early_fraud_warnings` | error | planned | read_many |
| GET | `/v1/radar/early_fraud_warnings/{early_fraud_warning}` | radar.early_fraud_warning | planned | read_one |
| GET | `/v1/radar/value_list_items` | error | planned | read_many |
| GET | `/v1/radar/value_list_items/{item}` | radar.value_list_item | planned | read_one |
| GET | `/v1/radar/value_lists` | error | planned | read_many |
| GET | `/v1/radar/value_lists/{value_list}` | radar.value_list | planned | read_one |
| GET | `/v1/refunds` | error | planned | read_many |
| GET | `/v1/refunds/{refund}` | refund | planned | read_one |
| GET | `/v1/reporting/report_runs` | error | planned | read_many |
| GET | `/v1/reporting/report_runs/{report_run}` | reporting.report_run | planned | read_one |
| GET | `/v1/reporting/report_types` | error | planned | read_many |
| GET | `/v1/reporting/report_types/{report_type}` | reporting.report_type | planned | read_one |
| GET | `/v1/reviews` | error | planned | read_many |
| GET | `/v1/reviews/{review}` | review | planned | read_one |
| GET | `/v1/setup_attempts` | error | planned | read_many |
| GET | `/v1/setup_intents` | error | planned | read_many |
| GET | `/v1/setup_intents/{intent}` | setup_intent | planned | read_one |
| GET | `/v1/shipping_rates` | error | planned | read_many |
| GET | `/v1/shipping_rates/{shipping_rate_token}` | shipping_rate | planned | read_one |
| GET | `/v1/sigma/scheduled_query_runs` | error | planned | read_many |
| GET | `/v1/sigma/scheduled_query_runs/{scheduled_query_run}` | scheduled_query_run | planned | read_one |
| GET | `/v1/sources/{source}` | source | planned | read_one |
| GET | `/v1/sources/{source}/mandate_notifications/{mandate_notification}` | source_mandate_notification | planned | read_one |
| GET | `/v1/sources/{source}/source_transactions` | error | planned | read_one |
| GET | `/v1/sources/{source}/source_transactions/{source_transaction}` | source_transaction | planned | read_one |
| GET | `/v1/subscription_items` | error | planned | read_many |
| GET | `/v1/subscription_items/{item}` | subscription_item | planned | read_one |
| GET | `/v1/subscription_items/{subscription_item}/usage_record_summaries` | error | planned | read_one |
| GET | `/v1/subscription_schedules` | error | planned | read_many |
| GET | `/v1/subscription_schedules/{schedule}` | subscription_schedule | planned | read_one |
| GET | `/v1/subscriptions` | error | planned | read_many |
| GET | `/v1/subscriptions/search` | error | planned | read_many |
| GET | `/v1/subscriptions/{subscription_exposed_id}` | subscription | planned | read_one |
| GET | `/v1/tax/calculations/{calculation}` | tax.calculation | planned | read_one |
| GET | `/v1/tax/calculations/{calculation}/line_items` | error | planned | read_one |
| GET | `/v1/tax/registrations` | error | planned | read_many |
| GET | `/v1/tax/registrations/{id}` | tax.registration | planned | read_one |
| GET | `/v1/tax/settings` | tax.settings | planned | read_many |
| GET | `/v1/tax/transactions/{transaction}` | tax.transaction | planned | read_one |
| GET | `/v1/tax/transactions/{transaction}/line_items` | error | planned | read_one |
| GET | `/v1/tax_codes` | error | planned | read_many |
| GET | `/v1/tax_codes/{id}` | tax_code | planned | read_one |
| GET | `/v1/tax_ids` | error | planned | read_many |
| GET | `/v1/tax_ids/{id}` | tax_id | planned | read_one |
| GET | `/v1/tax_rates` | error | planned | read_many |
| GET | `/v1/tax_rates/{tax_rate}` | tax_rate | planned | read_one |
| GET | `/v1/terminal/configurations` | error | planned | read_many |
| GET | `/v1/terminal/configurations/{configuration}` | error | planned | read_one |
| GET | `/v1/terminal/locations` | error | planned | read_many |
| GET | `/v1/terminal/locations/{location}` | error | planned | read_one |
| GET | `/v1/terminal/readers` | error | planned | read_many |
| GET | `/v1/terminal/readers/{reader}` | error | planned | read_one |
| GET | `/v1/test_helpers/test_clocks` | error | planned | read_many |
| GET | `/v1/test_helpers/test_clocks/{test_clock}` | test_helpers.test_clock | planned | read_one |
| GET | `/v1/tokens/{token}` | token | planned | read_one |
| GET | `/v1/topups` | error | planned | read_many |
| GET | `/v1/topups/{topup}` | topup | planned | read_one |
| GET | `/v1/transfers` | error | planned | read_many |
| GET | `/v1/transfers/{id}/reversals` | error | planned | read_one |
| GET | `/v1/transfers/{transfer}` | transfer | planned | read_one |
| GET | `/v1/transfers/{transfer}/reversals/{id}` | transfer_reversal | planned | read_one |
| GET | `/v1/treasury/credit_reversals` | error | planned | read_many |
| GET | `/v1/treasury/credit_reversals/{credit_reversal}` | treasury.credit_reversal | planned | read_one |
| GET | `/v1/treasury/debit_reversals` | error | planned | read_many |
| GET | `/v1/treasury/debit_reversals/{debit_reversal}` | treasury.debit_reversal | planned | read_one |
| GET | `/v1/treasury/financial_accounts` | error | planned | read_many |
| GET | `/v1/treasury/financial_accounts/{financial_account}` | treasury.financial_account | planned | read_one |
| GET | `/v1/treasury/financial_accounts/{financial_account}/features` | treasury.financial_account_features | planned | read_one |
| GET | `/v1/treasury/inbound_transfers` | error | planned | read_many |
| GET | `/v1/treasury/inbound_transfers/{id}` | treasury.inbound_transfer | planned | read_one |
| GET | `/v1/treasury/outbound_payments` | error | planned | read_many |
| GET | `/v1/treasury/outbound_payments/{id}` | treasury.outbound_payment | planned | read_one |
| GET | `/v1/treasury/outbound_transfers` | error | planned | read_many |
| GET | `/v1/treasury/outbound_transfers/{outbound_transfer}` | treasury.outbound_transfer | planned | read_one |
| GET | `/v1/treasury/received_credits` | error | planned | read_many |
| GET | `/v1/treasury/received_credits/{id}` | treasury.received_credit | planned | read_one |
| GET | `/v1/treasury/received_debits` | error | planned | read_many |
| GET | `/v1/treasury/received_debits/{id}` | treasury.received_debit | planned | read_one |
| GET | `/v1/treasury/transaction_entries` | error | planned | read_many |
| GET | `/v1/treasury/transaction_entries/{id}` | treasury.transaction_entry | planned | read_one |
| GET | `/v1/treasury/transactions` | error | planned | read_many |
| GET | `/v1/treasury/transactions/{id}` | treasury.transaction | planned | read_one |
| GET | `/v1/webhook_endpoints` | error | planned | read_many |
| GET | `/v1/webhook_endpoints/{webhook_endpoint}` | webhook_endpoint | planned | read_one |
| POST | `/v1/account_links` | account_link | planned | create |
| POST | `/v1/account_sessions` | account_session | planned | create |
| POST | `/v1/accounts` | account | planned | create |
| POST | `/v1/accounts/{account}` | account | planned | create |
| POST | `/v1/accounts/{account}/bank_accounts` | external_account | planned | create |
| POST | `/v1/accounts/{account}/bank_accounts/{id}` | external_account | planned | create |
| POST | `/v1/accounts/{account}/capabilities/{capability}` | capability | planned | create |
| POST | `/v1/accounts/{account}/external_accounts` | external_account | planned | create |
| POST | `/v1/accounts/{account}/external_accounts/{id}` | external_account | planned | create |
| POST | `/v1/accounts/{account}/login_links` | login_link | planned | create |
| POST | `/v1/accounts/{account}/people` | person | planned | create |
| POST | `/v1/accounts/{account}/people/{person}` | person | planned | create |
| POST | `/v1/accounts/{account}/persons` | person | planned | create |
| POST | `/v1/accounts/{account}/persons/{person}` | person | planned | create |
| POST | `/v1/accounts/{account}/reject` | account | planned | create |
| POST | `/v1/apple_pay/domains` | apple_pay_domain | planned | create |
| POST | `/v1/application_fees/{fee}/refunds/{id}` | fee_refund | planned | create |
| POST | `/v1/application_fees/{id}/refund` | application_fee | planned | create |
| POST | `/v1/application_fees/{id}/refunds` | fee_refund | planned | create |
| POST | `/v1/apps/secrets` | apps.secret | planned | create |
| POST | `/v1/apps/secrets/delete` | apps.secret | planned | create |
| POST | `/v1/billing/alerts` | billing.alert | planned | create |
| POST | `/v1/billing/alerts/{id}/activate` | billing.alert | planned | create |
| POST | `/v1/billing/alerts/{id}/archive` | billing.alert | planned | create |
| POST | `/v1/billing/alerts/{id}/deactivate` | billing.alert | planned | create |
| POST | `/v1/billing/credit_grants` | billing.credit_grant | planned | create |
| POST | `/v1/billing/credit_grants/{id}` | billing.credit_grant | planned | create |
| POST | `/v1/billing/credit_grants/{id}/expire` | billing.credit_grant | planned | create |
| POST | `/v1/billing/credit_grants/{id}/void` | billing.credit_grant | planned | create |
| POST | `/v1/billing/meter_event_adjustments` | billing.meter_event_adjustment | planned | create |
| POST | `/v1/billing/meter_events` | billing.meter_event | planned | create |
| POST | `/v1/billing/meters` | billing.meter | planned | create |
| POST | `/v1/billing/meters/{id}` | billing.meter | planned | create |
| POST | `/v1/billing/meters/{id}/deactivate` | billing.meter | planned | create |
| POST | `/v1/billing/meters/{id}/reactivate` | billing.meter | planned | create |
| POST | `/v1/billing_portal/configurations` | billing_portal.configuration | planned | create |
| POST | `/v1/billing_portal/configurations/{configuration}` | billing_portal.configuration | planned | create |
| POST | `/v1/billing_portal/sessions` | billing_portal.session | planned | create |
| POST | `/v1/charges` | charge | planned | create |
| POST | `/v1/charges/{charge}` | charge | planned | create |
| POST | `/v1/charges/{charge}/capture` | charge | planned | create |
| POST | `/v1/charges/{charge}/dispute` | dispute | planned | create |
| POST | `/v1/charges/{charge}/dispute/close` | dispute | planned | create |
| POST | `/v1/charges/{charge}/refund` | charge | planned | create |
| POST | `/v1/charges/{charge}/refunds` | refund | planned | create |
| POST | `/v1/charges/{charge}/refunds/{refund}` | refund | planned | create |
| POST | `/v1/checkout/sessions` | checkout.session | planned | create |
| POST | `/v1/checkout/sessions/{session}` | checkout.session | planned | create |
| POST | `/v1/checkout/sessions/{session}/expire` | checkout.session | planned | create |
| POST | `/v1/climate/orders` | climate.order | planned | create |
| POST | `/v1/climate/orders/{order}` | climate.order | planned | create |
| POST | `/v1/climate/orders/{order}/cancel` | climate.order | planned | create |
| POST | `/v1/coupons` | coupon | planned | create |
| POST | `/v1/coupons/{coupon}` | coupon | planned | create |
| POST | `/v1/credit_notes` | credit_note | planned | create |
| POST | `/v1/credit_notes/{id}` | credit_note | planned | create |
| POST | `/v1/credit_notes/{id}/void` | credit_note | planned | create |
| POST | `/v1/customer_sessions` | customer_session | planned | create |
| POST | `/v1/customers` | customer | planned | create |
| POST | `/v1/customers/{customer}` | customer | planned | create |
| POST | `/v1/customers/{customer}/balance_transactions` | customer_balance_transaction | planned | create |
| POST | `/v1/customers/{customer}/balance_transactions/{transaction}` | customer_balance_transaction | planned | create |
| POST | `/v1/customers/{customer}/bank_accounts` | payment_source | planned | create |
| POST | `/v1/customers/{customer}/bank_accounts/{id}` | error | planned | create |
| POST | `/v1/customers/{customer}/bank_accounts/{id}/verify` | bank_account | planned | create |
| POST | `/v1/customers/{customer}/cards` | payment_source | planned | create |
| POST | `/v1/customers/{customer}/cards/{id}` | error | planned | create |
| POST | `/v1/customers/{customer}/cash_balance` | cash_balance | planned | create |
| POST | `/v1/customers/{customer}/funding_instructions` | funding_instructions | planned | create |
| POST | `/v1/customers/{customer}/sources` | payment_source | planned | create |
| POST | `/v1/customers/{customer}/sources/{id}` | error | planned | create |
| POST | `/v1/customers/{customer}/sources/{id}/verify` | bank_account | planned | create |
| POST | `/v1/customers/{customer}/subscriptions` | subscription | planned | create |
| POST | `/v1/customers/{customer}/subscriptions/{subscription_exposed_id}` | subscription | planned | create |
| POST | `/v1/customers/{customer}/tax_ids` | tax_id | planned | create |
| POST | `/v1/disputes/{dispute}` | dispute | planned | create |
| POST | `/v1/disputes/{dispute}/close` | dispute | planned | create |
| POST | `/v1/entitlements/features` | entitlements.feature | planned | create |
| POST | `/v1/entitlements/features/{id}` | entitlements.feature | planned | create |
| POST | `/v1/ephemeral_keys` | ephemeral_key | planned | create |
| POST | `/v1/file_links` | file_link | planned | create |
| POST | `/v1/file_links/{link}` | file_link | planned | create |
| POST | `/v1/files` | file | planned | create |
| POST | `/v1/financial_connections/accounts/{account}/disconnect` | financial_connections.account | planned | create |
| POST | `/v1/financial_connections/accounts/{account}/refresh` | financial_connections.account | planned | create |
| POST | `/v1/financial_connections/accounts/{account}/subscribe` | financial_connections.account | planned | create |
| POST | `/v1/financial_connections/accounts/{account}/unsubscribe` | financial_connections.account | planned | create |
| POST | `/v1/financial_connections/sessions` | financial_connections.session | planned | create |
| POST | `/v1/forwarding/requests` | forwarding.request | planned | create |
| POST | `/v1/identity/verification_sessions` | identity.verification_session | planned | create |
| POST | `/v1/identity/verification_sessions/{session}` | identity.verification_session | planned | create |
| POST | `/v1/identity/verification_sessions/{session}/cancel` | identity.verification_session | planned | create |
| POST | `/v1/identity/verification_sessions/{session}/redact` | identity.verification_session | planned | create |
| POST | `/v1/invoice_rendering_templates/{template}/archive` | invoice_rendering_template | planned | create |
| POST | `/v1/invoice_rendering_templates/{template}/unarchive` | invoice_rendering_template | planned | create |
| POST | `/v1/invoiceitems` | invoiceitem | planned | create |
| POST | `/v1/invoiceitems/{invoiceitem}` | invoiceitem | planned | create |
| POST | `/v1/invoices` | invoice | planned | create |
| POST | `/v1/invoices/create_preview` | invoice | planned | create |
| POST | `/v1/invoices/{invoice}` | invoice | planned | create |
| POST | `/v1/invoices/{invoice}/add_lines` | invoice | planned | create |
| POST | `/v1/invoices/{invoice}/finalize` | invoice | planned | create |
| POST | `/v1/invoices/{invoice}/lines/{line_item_id}` | line_item | planned | create |
| POST | `/v1/invoices/{invoice}/mark_uncollectible` | invoice | planned | create |
| POST | `/v1/invoices/{invoice}/pay` | invoice | planned | create |
| POST | `/v1/invoices/{invoice}/remove_lines` | invoice | planned | create |
| POST | `/v1/invoices/{invoice}/send` | invoice | planned | create |
| POST | `/v1/invoices/{invoice}/update_lines` | invoice | planned | create |
| POST | `/v1/invoices/{invoice}/void` | invoice | planned | create |
| POST | `/v1/issuing/authorizations/{authorization}` | issuing.authorization | planned | create |
| POST | `/v1/issuing/authorizations/{authorization}/approve` | issuing.authorization | planned | create |
| POST | `/v1/issuing/authorizations/{authorization}/decline` | issuing.authorization | planned | create |
| POST | `/v1/issuing/cardholders` | issuing.cardholder | planned | create |
| POST | `/v1/issuing/cardholders/{cardholder}` | issuing.cardholder | planned | create |
| POST | `/v1/issuing/cards` | issuing.card | planned | create |
| POST | `/v1/issuing/cards/{card}` | issuing.card | planned | create |
| POST | `/v1/issuing/disputes` | issuing.dispute | planned | create |
| POST | `/v1/issuing/disputes/{dispute}` | issuing.dispute | planned | create |
| POST | `/v1/issuing/disputes/{dispute}/submit` | issuing.dispute | planned | create |
| POST | `/v1/issuing/personalization_designs` | issuing.personalization_design | planned | create |
| POST | `/v1/issuing/personalization_designs/{personalization_design}` | issuing.personalization_design | planned | create |
| POST | `/v1/issuing/settlements/{settlement}` | issuing.settlement | planned | create |
| POST | `/v1/issuing/tokens/{token}` | issuing.token | planned | create |
| POST | `/v1/issuing/transactions/{transaction}` | issuing.transaction | planned | create |
| POST | `/v1/link_account_sessions` | financial_connections.session | planned | create |
| POST | `/v1/linked_accounts/{account}/disconnect` | financial_connections.account | planned | create |
| POST | `/v1/linked_accounts/{account}/refresh` | financial_connections.account | planned | create |
| POST | `/v1/payment_intents` | payment_intent | planned | create |
| POST | `/v1/payment_intents/{intent}` | payment_intent | planned | create |
| POST | `/v1/payment_intents/{intent}/apply_customer_balance` | payment_intent | planned | create |
| POST | `/v1/payment_intents/{intent}/cancel` | payment_intent | planned | create |
| POST | `/v1/payment_intents/{intent}/capture` | payment_intent | planned | create |
| POST | `/v1/payment_intents/{intent}/confirm` | payment_intent | planned | create |
| POST | `/v1/payment_intents/{intent}/increment_authorization` | payment_intent | planned | create |
| POST | `/v1/payment_intents/{intent}/verify_microdeposits` | payment_intent | planned | create |
| POST | `/v1/payment_links` | payment_link | planned | create |
| POST | `/v1/payment_links/{payment_link}` | payment_link | planned | create |
| POST | `/v1/payment_method_configurations` | payment_method_configuration | planned | create |
| POST | `/v1/payment_method_configurations/{configuration}` | payment_method_configuration | planned | create |
| POST | `/v1/payment_method_domains` | payment_method_domain | planned | create |
| POST | `/v1/payment_method_domains/{payment_method_domain}` | payment_method_domain | planned | create |
| POST | `/v1/payment_method_domains/{payment_method_domain}/validate` | payment_method_domain | planned | create |
| POST | `/v1/payment_methods` | payment_method | planned | create |
| POST | `/v1/payment_methods/{payment_method}` | payment_method | planned | create |
| POST | `/v1/payment_methods/{payment_method}/attach` | payment_method | planned | create |
| POST | `/v1/payment_methods/{payment_method}/detach` | payment_method | planned | create |
| POST | `/v1/payouts` | payout | planned | create |
| POST | `/v1/payouts/{payout}` | payout | planned | create |
| POST | `/v1/payouts/{payout}/cancel` | payout | planned | create |
| POST | `/v1/payouts/{payout}/reverse` | payout | planned | create |
| POST | `/v1/plans` | plan | planned | create |
| POST | `/v1/plans/{plan}` | plan | planned | create |
| POST | `/v1/prices` | price | planned | create |
| POST | `/v1/prices/{price}` | price | planned | create |
| POST | `/v1/products` | product | planned | create |
| POST | `/v1/products/{id}` | product | planned | create |
| POST | `/v1/products/{product}/features` | product_feature | planned | create |
| POST | `/v1/promotion_codes` | promotion_code | planned | create |
| POST | `/v1/promotion_codes/{promotion_code}` | promotion_code | planned | create |
| POST | `/v1/quotes` | quote | planned | create |
| POST | `/v1/quotes/{quote}` | quote | planned | create |
| POST | `/v1/quotes/{quote}/accept` | quote | planned | create |
| POST | `/v1/quotes/{quote}/cancel` | quote | planned | create |
| POST | `/v1/quotes/{quote}/finalize` | quote | planned | create |
| POST | `/v1/radar/value_list_items` | radar.value_list_item | planned | create |
| POST | `/v1/radar/value_lists` | radar.value_list | planned | create |
| POST | `/v1/radar/value_lists/{value_list}` | radar.value_list | planned | create |
| POST | `/v1/refunds` | refund | planned | create |
| POST | `/v1/refunds/{refund}` | refund | planned | create |
| POST | `/v1/refunds/{refund}/cancel` | refund | planned | create |
| POST | `/v1/reporting/report_runs` | reporting.report_run | planned | create |
| POST | `/v1/reviews/{review}/approve` | review | planned | create |
| POST | `/v1/setup_intents` | setup_intent | planned | create |
| POST | `/v1/setup_intents/{intent}` | setup_intent | planned | create |
| POST | `/v1/setup_intents/{intent}/cancel` | setup_intent | planned | create |
| POST | `/v1/setup_intents/{intent}/confirm` | setup_intent | planned | create |
| POST | `/v1/setup_intents/{intent}/verify_microdeposits` | setup_intent | planned | create |
| POST | `/v1/shipping_rates` | shipping_rate | planned | create |
| POST | `/v1/shipping_rates/{shipping_rate_token}` | shipping_rate | planned | create |
| POST | `/v1/sources` | source | planned | create |
| POST | `/v1/sources/{source}` | source | planned | create |
| POST | `/v1/sources/{source}/verify` | source | planned | create |
| POST | `/v1/subscription_items` | subscription_item | planned | create |
| POST | `/v1/subscription_items/{item}` | subscription_item | planned | create |
| POST | `/v1/subscription_items/{subscription_item}/usage_records` | usage_record | planned | create |
| POST | `/v1/subscription_schedules` | subscription_schedule | planned | create |
| POST | `/v1/subscription_schedules/{schedule}` | subscription_schedule | planned | create |
| POST | `/v1/subscription_schedules/{schedule}/cancel` | subscription_schedule | planned | create |
| POST | `/v1/subscription_schedules/{schedule}/release` | subscription_schedule | planned | create |
| POST | `/v1/subscriptions` | subscription | planned | create |
| POST | `/v1/subscriptions/{subscription_exposed_id}` | subscription | planned | create |
| POST | `/v1/subscriptions/{subscription}/resume` | subscription | planned | create |
| POST | `/v1/tax/calculations` | tax.calculation | planned | create |
| POST | `/v1/tax/registrations` | tax.registration | planned | create |
| POST | `/v1/tax/registrations/{id}` | tax.registration | planned | create |
| POST | `/v1/tax/settings` | tax.settings | planned | create |
| POST | `/v1/tax/transactions/create_from_calculation` | tax.transaction | planned | create |
| POST | `/v1/tax/transactions/create_reversal` | tax.transaction | planned | create |
| POST | `/v1/tax_ids` | tax_id | planned | create |
| POST | `/v1/tax_rates` | tax_rate | planned | create |
| POST | `/v1/tax_rates/{tax_rate}` | tax_rate | planned | create |
| POST | `/v1/terminal/configurations` | terminal.configuration | planned | create |
| POST | `/v1/terminal/configurations/{configuration}` | error | planned | create |
| POST | `/v1/terminal/connection_tokens` | terminal.connection_token | planned | create |
| POST | `/v1/terminal/locations` | terminal.location | planned | create |
| POST | `/v1/terminal/locations/{location}` | error | planned | create |
| POST | `/v1/terminal/readers` | terminal.reader | planned | create |
| POST | `/v1/terminal/readers/{reader}` | error | planned | create |
| POST | `/v1/terminal/readers/{reader}/cancel_action` | terminal.reader | planned | create |
| POST | `/v1/terminal/readers/{reader}/process_payment_intent` | terminal.reader | planned | create |
| POST | `/v1/terminal/readers/{reader}/process_setup_intent` | terminal.reader | planned | create |
| POST | `/v1/terminal/readers/{reader}/refund_payment` | terminal.reader | planned | create |
| POST | `/v1/terminal/readers/{reader}/set_reader_display` | terminal.reader | planned | create |
| POST | `/v1/test_helpers/confirmation_tokens` | confirmation_token | planned | create |
| POST | `/v1/test_helpers/customers/{customer}/fund_cash_balance` | customer_cash_balance_transaction | planned | create |
| POST | `/v1/test_helpers/issuing/authorizations` | issuing.authorization | planned | create |
| POST | `/v1/test_helpers/issuing/authorizations/{authorization}/capture` | issuing.authorization | planned | create |
| POST | `/v1/test_helpers/issuing/authorizations/{authorization}/expire` | issuing.authorization | planned | create |
| POST | `/v1/test_helpers/issuing/authorizations/{authorization}/finalize_amount` | issuing.authorization | planned | create |
| POST | `/v1/test_helpers/issuing/authorizations/{authorization}/increment` | issuing.authorization | planned | create |
| POST | `/v1/test_helpers/issuing/authorizations/{authorization}/reverse` | issuing.authorization | planned | create |
| POST | `/v1/test_helpers/issuing/cards/{card}/shipping/deliver` | issuing.card | planned | create |
| POST | `/v1/test_helpers/issuing/cards/{card}/shipping/fail` | issuing.card | planned | create |
| POST | `/v1/test_helpers/issuing/cards/{card}/shipping/return` | issuing.card | planned | create |
| POST | `/v1/test_helpers/issuing/cards/{card}/shipping/ship` | issuing.card | planned | create |
| POST | `/v1/test_helpers/issuing/personalization_designs/{personalization_design}/activate` | issuing.personalization_design | planned | create |
| POST | `/v1/test_helpers/issuing/personalization_designs/{personalization_design}/deactivate` | issuing.personalization_design | planned | create |
| POST | `/v1/test_helpers/issuing/personalization_designs/{personalization_design}/reject` | issuing.personalization_design | planned | create |
| POST | `/v1/test_helpers/issuing/settlements` | issuing.settlement | planned | create |
| POST | `/v1/test_helpers/issuing/transactions/create_force_capture` | issuing.transaction | planned | create |
| POST | `/v1/test_helpers/issuing/transactions/create_unlinked_refund` | issuing.transaction | planned | create |
| POST | `/v1/test_helpers/issuing/transactions/{transaction}/refund` | issuing.transaction | planned | create |
| POST | `/v1/test_helpers/refunds/{refund}/expire` | refund | planned | create |
| POST | `/v1/test_helpers/terminal/readers/{reader}/present_payment_method` | terminal.reader | planned | create |
| POST | `/v1/test_helpers/test_clocks` | test_helpers.test_clock | planned | create |
| POST | `/v1/test_helpers/test_clocks/{test_clock}/advance` | test_helpers.test_clock | planned | create |
| POST | `/v1/test_helpers/treasury/inbound_transfers/{id}/fail` | treasury.inbound_transfer | planned | create |
| POST | `/v1/test_helpers/treasury/inbound_transfers/{id}/return` | treasury.inbound_transfer | planned | create |
| POST | `/v1/test_helpers/treasury/inbound_transfers/{id}/succeed` | treasury.inbound_transfer | planned | create |
| POST | `/v1/test_helpers/treasury/outbound_payments/{id}` | treasury.outbound_payment | planned | create |
| POST | `/v1/test_helpers/treasury/outbound_payments/{id}/fail` | treasury.outbound_payment | planned | create |
| POST | `/v1/test_helpers/treasury/outbound_payments/{id}/post` | treasury.outbound_payment | planned | create |
| POST | `/v1/test_helpers/treasury/outbound_payments/{id}/return` | treasury.outbound_payment | planned | create |
| POST | `/v1/test_helpers/treasury/outbound_transfers/{outbound_transfer}` | treasury.outbound_transfer | planned | create |
| POST | `/v1/test_helpers/treasury/outbound_transfers/{outbound_transfer}/fail` | treasury.outbound_transfer | planned | create |
| POST | `/v1/test_helpers/treasury/outbound_transfers/{outbound_transfer}/post` | treasury.outbound_transfer | planned | create |
| POST | `/v1/test_helpers/treasury/outbound_transfers/{outbound_transfer}/return` | treasury.outbound_transfer | planned | create |
| POST | `/v1/test_helpers/treasury/received_credits` | treasury.received_credit | planned | create |
| POST | `/v1/test_helpers/treasury/received_debits` | treasury.received_debit | planned | create |
| POST | `/v1/tokens` | token | planned | create |
| POST | `/v1/topups` | topup | planned | create |
| POST | `/v1/topups/{topup}` | topup | planned | create |
| POST | `/v1/topups/{topup}/cancel` | topup | planned | create |
| POST | `/v1/transfers` | transfer | planned | create |
| POST | `/v1/transfers/{id}/reversals` | transfer_reversal | planned | create |
| POST | `/v1/transfers/{transfer}` | transfer | planned | create |
| POST | `/v1/transfers/{transfer}/reversals/{id}` | transfer_reversal | planned | create |
| POST | `/v1/treasury/credit_reversals` | treasury.credit_reversal | planned | create |
| POST | `/v1/treasury/debit_reversals` | treasury.debit_reversal | planned | create |
| POST | `/v1/treasury/financial_accounts` | treasury.financial_account | planned | create |
| POST | `/v1/treasury/financial_accounts/{financial_account}` | treasury.financial_account | planned | create |
| POST | `/v1/treasury/financial_accounts/{financial_account}/features` | treasury.financial_account_features | planned | create |
| POST | `/v1/treasury/inbound_transfers` | treasury.inbound_transfer | planned | create |
| POST | `/v1/treasury/inbound_transfers/{inbound_transfer}/cancel` | treasury.inbound_transfer | planned | create |
| POST | `/v1/treasury/outbound_payments` | treasury.outbound_payment | planned | create |
| POST | `/v1/treasury/outbound_payments/{id}/cancel` | treasury.outbound_payment | planned | create |
| POST | `/v1/treasury/outbound_transfers` | treasury.outbound_transfer | planned | create |
| POST | `/v1/treasury/outbound_transfers/{outbound_transfer}/cancel` | treasury.outbound_transfer | planned | create |
| POST | `/v1/webhook_endpoints` | webhook_endpoint | planned | create |
| POST | `/v1/webhook_endpoints/{webhook_endpoint}` | webhook_endpoint | planned | create |
