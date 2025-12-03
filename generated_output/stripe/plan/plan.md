# Reverse Engineering Plan for `stripe`

**Total Routes:** 559
**Generated At:** 2025-12-03T19:57:03.918554+00:00

## Agent Directives
1. Review the component summary below to understand the CRUD surface.
2. Use component-specific plans in `plan/components/` for detailed route information.
3. Implement server handlers that satisfy the described operations and filters.
4. Raise any ambiguities called out in validation warnings before coding.

## Validation Summary
### Errors
- ⚠️ Missing component mapping for GET /v1/accounts/{account}/people.
- ⚠️ Missing component mapping for DELETE /v1/accounts/{account}/people/{person}.
- ⚠️ Missing component mapping for GET /v1/apple_pay/domains.
- ⚠️ Missing component mapping for DELETE /v1/apple_pay/domains/{domain}.
- ⚠️ Missing component mapping for GET /v1/apps/secrets.
- ⚠️ Missing component mapping for GET /v1/balance/history.
- ⚠️ Missing component mapping for GET /v1/billing/alerts.
- ⚠️ Missing component mapping for GET /v1/billing/credit_balance_transactions.
- ⚠️ Missing component mapping for GET /v1/billing/credit_grants.
- ⚠️ Missing component mapping for GET /v1/billing/meters.
- ... and 65 more errors
### Warnings
- ⚠️ No component mapping found for GET /v1/accounts/{account}/people.
- ⚠️ No component mapping found for DELETE /v1/accounts/{account}/people/{person}.
- ⚠️ No component mapping found for GET /v1/apple_pay/domains.
- ⚠️ No component mapping found for DELETE /v1/apple_pay/domains/{domain}.
- ⚠️ No component mapping found for GET /v1/apps/secrets.
- ⚠️ No component mapping found for GET /v1/balance/history.
- ⚠️ No component mapping found for GET /v1/billing/alerts.
- ⚠️ No component mapping found for GET /v1/billing/credit_balance_transactions.
- ⚠️ No component mapping found for GET /v1/billing/credit_grants.
- ⚠️ No component mapping found for GET /v1/billing/meters.
- ... and 65 more warnings

## Component Summary

Each component below has a dedicated plan file in `plan/components/` with detailed route information.

| Component | Operations | Route Count | Plan File |
|-----------|------------|-------------|-----------|
| `account` | `create`, `read_one`, `read_many`, `delete` | 8 | `plan/components/account.md` |
| `account_link` | `create` | 1 | `plan/components/account_link.md` |
| `account_session` | `create` | 1 | `plan/components/account_session.md` |
| `apple_pay_domain` | `create`, `read_one` | 2 | `plan/components/apple_pay_domain.md` |
| `application_fee` | `create`, `read_one`, `read_many` | 3 | `plan/components/application_fee.md` |
| `apps.secret` | `create`, `read_many` | 3 | `plan/components/apps_secret.md` |
| `balance` | `read_many` | 1 | `plan/components/balance.md` |
| `balance_transaction` | `read_one`, `read_many` | 4 | `plan/components/balance_transaction.md` |
| `bank_account` | `create`, `read_one`, `delete` | 7 | `plan/components/bank_account.md` |
| `billing.alert` | `create`, `read_one` | 5 | `plan/components/billing_alert.md` |
| `billing.credit_balance_summary` | `read_many` | 1 | `plan/components/billing_credit_balance_summary.md` |
| `billing.credit_balance_transaction` | `read_one` | 1 | `plan/components/billing_credit_balance_transaction.md` |
| `billing.credit_grant` | `create`, `read_one` | 5 | `plan/components/billing_credit_grant.md` |
| `billing.meter` | `create`, `read_one` | 5 | `plan/components/billing_meter.md` |
| `billing.meter_event` | `create` | 1 | `plan/components/billing_meter_event.md` |
| `billing.meter_event_adjustment` | `create` | 1 | `plan/components/billing_meter_event_adjustment.md` |
| `billing_portal.configuration` | `create`, `read_one` | 3 | `plan/components/billing_portal_configuration.md` |
| `billing_portal.session` | `create` | 1 | `plan/components/billing_portal_session.md` |
| `capability` | `create`, `read_one` | 3 | `plan/components/capability.md` |
| `card` | `create`, `read_one`, `read_many`, `delete` | 5 | `plan/components/card.md` |
| `cash_balance` | `create`, `read_one` | 2 | `plan/components/cash_balance.md` |
| `charge` | `create`, `read_one`, `read_many` | 6 | `plan/components/charge.md` |
| `checkout.session` | `create`, `read_one` | 4 | `plan/components/checkout_session.md` |
| `climate.order` | `create`, `read_one` | 4 | `plan/components/climate_order.md` |
| `climate.product` | `read_one` | 1 | `plan/components/climate_product.md` |
| `climate.supplier` | `read_one` | 1 | `plan/components/climate_supplier.md` |
| `confirmation_token` | `create`, `read_one` | 2 | `plan/components/confirmation_token.md` |
| `country_spec` | `read_one`, `read_many` | 2 | `plan/components/country_spec.md` |
| `coupon` | `create`, `read_one`, `read_many`, `delete` | 5 | `plan/components/coupon.md` |
| `credit_note` | `create`, `read_one`, `read_many` | 6 | `plan/components/credit_note.md` |
| `customer` | `create`, `read_one`, `read_many`, `delete` | 5 | `plan/components/customer.md` |
| `customer_balance_transaction` | `create`, `read_one` | 3 | `plan/components/customer_balance_transaction.md` |
| `customer_cash_balance_transaction` | `create`, `read_one` | 2 | `plan/components/customer_cash_balance_transaction.md` |
| `customer_session` | `create` | 1 | `plan/components/customer_session.md` |
| `discount` | `read_one`, `delete` | 5 | `plan/components/discount.md` |
| `dispute` | `create`, `read_one`, `read_many` | 8 | `plan/components/dispute.md` |
| `entitlements.active_entitlement` | `read_one` | 1 | `plan/components/entitlements_active_entitlement.md` |
| `entitlements.feature` | `create`, `read_one` | 3 | `plan/components/entitlements_feature.md` |
| `ephemeral_key` | `create`, `delete` | 2 | `plan/components/ephemeral_key.md` |
| `event` | `read_one`, `read_many` | 2 | `plan/components/event.md` |
| `exchange_rate` | `read_one`, `read_many` | 2 | `plan/components/exchange_rate.md` |
| `external_account` | `create`, `read_one`, `delete` | 8 | `plan/components/external_account.md` |
| `fee_refund` | `create`, `read_one` | 3 | `plan/components/fee_refund.md` |
| `file` | `create`, `read_one`, `read_many` | 3 | `plan/components/file.md` |
| `file_link` | `create`, `read_one`, `read_many` | 4 | `plan/components/file_link.md` |
| `financial_connections.account` | `create`, `read_one` | 8 | `plan/components/financial_connections_account.md` |
| `financial_connections.session` | `create`, `read_one` | 4 | `plan/components/financial_connections_session.md` |
| `financial_connections.transaction` | `read_one` | 1 | `plan/components/financial_connections_transaction.md` |
| `forwarding.request` | `create`, `read_one` | 2 | `plan/components/forwarding_request.md` |
| `funding_instructions` | `create` | 1 | `plan/components/funding_instructions.md` |
| `identity.verification_report` | `read_one` | 1 | `plan/components/identity_verification_report.md` |
| `identity.verification_session` | `create`, `read_one` | 5 | `plan/components/identity_verification_session.md` |
| `inbound_transfers` | `read_many` | 1 | `plan/components/inbound_transfers.md` |
| `invoice` | `create`, `read_one`, `read_many`, `delete` | 15 | `plan/components/invoice.md` |
| `invoice_rendering_template` | `create`, `read_one`, `read_many` | 4 | `plan/components/invoice_rendering_template.md` |
| `invoiceitem` | `create`, `read_one`, `read_many`, `delete` | 5 | `plan/components/invoiceitem.md` |
| `issuing.authorization` | `create`, `read_one` | 10 | `plan/components/issuing_authorization.md` |
| `issuing.card` | `create`, `read_one` | 7 | `plan/components/issuing_card.md` |
| `issuing.cardholder` | `create`, `read_one` | 3 | `plan/components/issuing_cardholder.md` |
| `issuing.dispute` | `create`, `read_one` | 4 | `plan/components/issuing_dispute.md` |
| `issuing.personalization_design` | `create`, `read_one` | 6 | `plan/components/issuing_personalization_design.md` |
| `issuing.physical_bundle` | `read_one` | 1 | `plan/components/issuing_physical_bundle.md` |
| `issuing.settlement` | `create`, `read_one` | 3 | `plan/components/issuing_settlement.md` |
| `issuing.token` | `create`, `read_one` | 2 | `plan/components/issuing_token.md` |
| `issuing.transaction` | `create`, `read_one` | 5 | `plan/components/issuing_transaction.md` |
| `line_item` | `create`, `read_one` | 6 | `plan/components/line_item.md` |
| `login_link` | `create` | 1 | `plan/components/login_link.md` |
| `mandate` | `read_one` | 1 | `plan/components/mandate.md` |
| `outbound_payments_payment_method_details` | `read_many` | 1 | `plan/components/outbound_payments_payment_method_details.md` |
| `outbound_transfers_payment_method_details` | `read_many` | 1 | `plan/components/outbound_transfers_payment_method_details.md` |
| `payment_intent` | `create`, `read_one`, `read_many` | 10 | `plan/components/payment_intent.md` |
| `payment_link` | `create`, `read_one`, `read_many` | 4 | `plan/components/payment_link.md` |
| `payment_method` | `create`, `read_one`, `read_many` | 8 | `plan/components/payment_method.md` |
| `payment_method_configuration` | `create`, `read_one`, `read_many` | 4 | `plan/components/payment_method_configuration.md` |
| `payment_method_domain` | `create`, `read_one`, `read_many` | 5 | `plan/components/payment_method_domain.md` |
| `payment_source` | `create`, `read_one` | 4 | `plan/components/payment_source.md` |
| `payout` | `create`, `read_one`, `read_many` | 6 | `plan/components/payout.md` |
| `person` | `create`, `read_one`, `delete` | 8 | `plan/components/person.md` |
| `plan` | `create`, `read_one`, `read_many`, `delete` | 5 | `plan/components/plan.md` |
| `price` | `create`, `read_one`, `read_many` | 4 | `plan/components/price.md` |
| `product` | `create`, `read_one`, `read_many`, `delete` | 6 | `plan/components/product.md` |
| `product_feature` | `create`, `read_one` | 2 | `plan/components/product_feature.md` |
| `promotion_code` | `create`, `read_one`, `read_many` | 4 | `plan/components/promotion_code.md` |
| `quote` | `create`, `read_one`, `read_many` | 7 | `plan/components/quote.md` |
| `radar.early_fraud_warning` | `read_one` | 1 | `plan/components/radar_early_fraud_warning.md` |
| `radar.value_list` | `create`, `read_one` | 3 | `plan/components/radar_value_list.md` |
| `radar.value_list_item` | `create`, `read_one` | 2 | `plan/components/radar_value_list_item.md` |
| `refund` | `create`, `read_one`, `read_many` | 11 | `plan/components/refund.md` |
| `reporting.report_run` | `create`, `read_one` | 2 | `plan/components/reporting_report_run.md` |
| `reporting.report_type` | `read_one` | 1 | `plan/components/reporting_report_type.md` |
| `review` | `create`, `read_one`, `read_many` | 3 | `plan/components/review.md` |
| `scheduled_query_run` | `read_one`, `read_many` | 2 | `plan/components/scheduled_query_run.md` |
| `setup_attempt` | `read_many` | 1 | `plan/components/setup_attempt.md` |
| `setup_intent` | `create`, `read_one`, `read_many` | 7 | `plan/components/setup_intent.md` |
| `shipping_rate` | `create`, `read_one`, `read_many` | 4 | `plan/components/shipping_rate.md` |
| `source` | `create`, `read_one`, `delete` | 7 | `plan/components/source.md` |
| `source_mandate_notification` | `read_one` | 1 | `plan/components/source_mandate_notification.md` |
| `source_transaction` | `read_one` | 2 | `plan/components/source_transaction.md` |
| `subscription` | `create`, `read_one`, `read_many`, `delete` | 11 | `plan/components/subscription.md` |
| `subscription_item` | `create`, `read_one`, `read_many`, `delete` | 5 | `plan/components/subscription_item.md` |
| `subscription_schedule` | `create`, `read_one`, `read_many` | 6 | `plan/components/subscription_schedule.md` |
| `tax.calculation` | `create`, `read_one` | 2 | `plan/components/tax_calculation.md` |
| `tax.registration` | `create`, `read_one` | 3 | `plan/components/tax_registration.md` |
| `tax.settings` | `create`, `read_many` | 2 | `plan/components/tax_settings.md` |
| `tax.transaction` | `create`, `read_one` | 3 | `plan/components/tax_transaction.md` |
| `tax_code` | `read_one`, `read_many` | 2 | `plan/components/tax_code.md` |
| `tax_id` | `create`, `read_one`, `read_many`, `delete` | 8 | `plan/components/tax_id.md` |
| `tax_rate` | `create`, `read_one`, `read_many` | 4 | `plan/components/tax_rate.md` |
| `terminal.configuration` | `create` | 1 | `plan/components/terminal_configuration.md` |
| `terminal.connection_token` | `create` | 1 | `plan/components/terminal_connection_token.md` |
| `terminal.location` | `create` | 1 | `plan/components/terminal_location.md` |
| `terminal.reader` | `create` | 7 | `plan/components/terminal_reader.md` |
| `test_helpers.test_clock` | `create`, `read_one` | 3 | `plan/components/test_helpers_test_clock.md` |
| `token` | `create`, `read_one`, `read_many` | 3 | `plan/components/token.md` |
| `topup` | `create`, `read_one`, `read_many` | 5 | `plan/components/topup.md` |
| `transfer` | `create`, `read_one`, `read_many` | 4 | `plan/components/transfer.md` |
| `transfer_reversal` | `create`, `read_one` | 3 | `plan/components/transfer_reversal.md` |
| `treasury.credit_reversal` | `create`, `read_one` | 2 | `plan/components/treasury_credit_reversal.md` |
| `treasury.debit_reversal` | `create`, `read_one` | 2 | `plan/components/treasury_debit_reversal.md` |
| `treasury.financial_account` | `create`, `read_one` | 3 | `plan/components/treasury_financial_account.md` |
| `treasury.financial_account_features` | `create`, `read_one` | 2 | `plan/components/treasury_financial_account_features.md` |
| `treasury.inbound_transfer` | `create`, `read_one` | 6 | `plan/components/treasury_inbound_transfer.md` |
| `treasury.outbound_payment` | `create`, `read_one` | 7 | `plan/components/treasury_outbound_payment.md` |
| `treasury.outbound_transfer` | `create`, `read_one` | 7 | `plan/components/treasury_outbound_transfer.md` |
| `treasury.received_credit` | `create`, `read_one` | 2 | `plan/components/treasury_received_credit.md` |
| `treasury.received_debit` | `create`, `read_one` | 2 | `plan/components/treasury_received_debit.md` |
| `treasury.transaction` | `read_one` | 1 | `plan/components/treasury_transaction.md` |
| `treasury.transaction_entry` | `read_one` | 1 | `plan/components/treasury_transaction_entry.md` |
| `usage_record` | `create` | 1 | `plan/components/usage_record.md` |
| `usage_record_summary` | `read_one` | 1 | `plan/components/usage_record_summary.md` |
| `webhook_endpoint` | `create`, `read_one`, `read_many`, `delete` | 5 | `plan/components/webhook_endpoint.md` |

## Quick Stats

**Operations by Type:**
- `create`: 267 routes
- `read_one`: 137 routes
- `read_many`: 57 routes
- `delete`: 23 routes

**Routes by Status:**
- `needs_mapping`: 75 routes
- `planned`: 484 routes

---

**Note:** For detailed route-by-route information, see individual component plan files in `plan/components/`.
