# Graph-Based Data Generation

This document explains how to generate realistic sample data for ALL components in an API using the component dependency graph.

## Overview

The graph-based generator:

1. **Builds a dependency graph** from the component registry
2. **Identifies leaves** (components with no dependencies - these are generated first)
3. **Generates data in topological order** (dependencies before dependents)
4. **Creates references** between components (foreign keys point to existing records)
5. **Uses GPT API** (optional) to generate realistic field values

## How It Works

### Step 1: Build Dependency Graph

```python
from ingestion import construct_component_graph

graph = construct_component_graph("stripe")
# Returns: {"nodes": [...], "edges": [...]}
```

The graph shows which components reference which:
- **Edge**: `source -> target` means `source` references `target` (source depends on target)
- **Leaves**: Components with `dependent_count = 0` (no other components depend on them)

### Step 2: Topological Sort

Components are sorted so dependencies come before dependents:

```
Leaves (no deps) → Intermediate → Roots (many dependents)
```

For example:
- `Address` (leaf) - no dependencies → Generate first
- `Customer` - references `Address` → Generate after `Address`
- `Order` - references `Customer` → Generate after `Customer`

### Step 3: Generate Records

For each component in order:

1. **Extract schema** properties from component registry
2. **For each reference**: Point to existing generated record
3. **For each field**: Generate value using:
   - GPT API (if available) - returns realistic values
   - Heuristics (fallback) - simple patterns based on field name/type

### Step 4: Store Data

Data can be stored:
- In database (`GeneratedRecord` table) - for main backend
- In account-scoped storage - for standalone APIs
- Returned as JSON - for application via HTTP

## Usage

### API Endpoint

```bash
curl -X POST "http://localhost:8000/reverse/generate_data" \
  -H "Content-Type: application/json" \
  -d '{
    "api_slug": "stripe",
    "use_graph": true,
    "counts": {
      "account": 5,
      "customer": 10,
      "charge": 20
    },
    "openai_api_key": "sk-...",
    "seed_account_id": "acct_123"
  }'
```

### Python API

```python
from reverse.graph_based_generator import GraphDataGenerator

generator = GraphDataGenerator(
    api_slug="stripe",
    openai_api_key="sk-..."  # Optional
)

# Generate data for all components
data = generator.generate_all(
    count_per_component={
        "account": 5,
        "customer": 10,
        "charge": 20
    },
    seed_account_id="acct_123"  # Optional - for account-scoped storage
)
```

### Via Data Synthesizer

```python
from reverse.data_synthesizer import synthesize_all_components

data = synthesize_all_components(
    api_slug="stripe",
    count_per_component={"account": 5, "customer": 10},
    openai_api_key="sk-...",
    seed_account_id="acct_123"
)
```

## GPT Integration

When `openai_api_key` is provided, the generator uses GPT-3.5-turbo to generate realistic values:

**Example prompts:**
- `username` → GPT returns: `"john_doe"`
- `email` → GPT returns: `"user@example.com"`
- `amount` → GPT returns: `100`
- `status` → GPT returns: `"active"`

**Fallback:** If GPT is unavailable or fails, uses heuristics:
- `username` → `user_0`
- `email` → `user0@example.com`
- `amount` → `100` (index * 100)

## Reference Handling

When a component references another:

```python
# Customer schema has: {"address": {"$ref": "#/components/schemas/Address"}}

# When generating Customer record:
address_ref = existing_address_records[index % len(existing_address_records)]
customer_record["address_id"] = address_ref["id"]
```

This ensures:
- All references point to existing records
- Referential integrity is maintained
- Data structure is coherent

## Example: Stripe API

### Dependency Order

1. **Leaves** (generate first):
   - `BalanceTransaction`
   - `CountrySpec`
   - `Currency`

2. **Intermediate** (generate after dependencies):
   - `Account` (may reference `CountrySpec`)
   - `Customer` (may reference `Account`)
   - `Charge` (references `Customer`)

3. **Roots** (generate last):
   - `PaymentIntent` (references many components)
   - `Subscription` (references `Customer`, `Plan`, etc.)

### Generated Data Structure

```python
{
    "balance_transaction": [
        {"id": "bt_1", "amount": 100, "currency": "usd"},
        {"id": "bt_2", "amount": 200, "currency": "usd"}
    ],
    "account": [
        {"id": "acct_1", "country": "US", ...},
        {"id": "acct_2", "country": "CA", ...}
    ],
    "customer": [
        {"id": "cus_1", "account_id": "acct_1", ...},  # References account
        {"id": "cus_2", "account_id": "acct_1", ...}   # References account
    ],
    "charge": [
        {"id": "ch_1", "customer": "cus_1", ...},  # References customer
        {"id": "ch_2", "customer": "cus_2", ...}   # References customer
    ]
}
```

## Storing in Runtime

For standalone APIs, store data in account-scoped storage:

```python
from runtime import insert_account_component_record

for component_name, records in data.items():
    for record in records:
        insert_account_component_record(
            account_id="acct_123",
            component_name=component_name,
            payload=record
        )
```

## Requirements

Add to `requirements.txt`:
```
openai>=1.0.0  # Optional - only needed for GPT generation
```

## Configuration

Set environment variable (optional):
```bash
export OPENAI_API_KEY="sk-..."
```

Or pass via API/function call.

## Benefits

1. **Complete Coverage**: Generates data for ALL components, not just route components
2. **Correct Order**: Respects dependencies (no broken references)
3. **Realistic Data**: GPT generates human-readable values
4. **Account Isolation**: Can generate per-account datasets
5. **Extensible**: Easy to add custom field generators

## Limitations

1. **GPT Costs**: Each field value requires an API call (can be expensive)
2. **Speed**: GPT calls add latency (use heuristics for faster generation)
3. **Cycles**: Components with circular dependencies may have issues (handled via fallback)

## Next Steps

1. Upload OpenAPI spec → Components registered
2. Call `/reverse/generate_data` with `use_graph=true`
3. Data is generated and can be stored in:
   - Database (via `GeneratedRecord`)
   - Runtime storage (via `insert_account_component_record`)
   - Returned as JSON response

See `backend/reverse/graph_based_generator.py` for implementation details.

