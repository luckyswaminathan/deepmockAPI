# How to Use Graph-Based Data Generation

Simple guide to generate realistic sample data for your API components.

## Quick Start

### 1. Set OpenAI API Key (Optional)

```bash
export OPENAI_API_KEY="sk-your-key-here"
```

**Note:** If you don't set this, the system will use heuristics (less realistic but faster and free).

### 2. Call the API Endpoint

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
    }
  }'
```

**Response:**
```json
{
  "api_slug": "stripe",
  "generated_at": "2024-01-15T10:30:00Z",
  "dataset": {
    "account": [
      {"id": "acct_1", "country": "US", "type": "standard", ...},
      {"id": "acct_2", "country": "CA", "type": "express", ...},
      ...
    ],
    "customer": [
      {"id": "cus_1", "email": "customer1@example.com", ...},
      ...
    ],
    ...
  }
}
```

## Step-by-Step Workflow

### Step 1: Upload Your OpenAPI Spec

```bash
curl -X POST "http://localhost:8000/apis/upload" \
  -F "spec_file=@stripe_api.json" \
  -F "api_name=Stripe API"
```

This registers all components in the database.

### Step 2: Generate Data for All Components

```bash
curl -X POST "http://localhost:8000/reverse/generate_data" \
  -H "Content-Type: application/json" \
  -d '{
    "api_slug": "stripe",
    "use_graph": true,
    "counts": {
      "account": 5,
      "customer": 10,
      "charge": 25,
      "subscription": 8
    }
  }'
```

**What happens:**
1. Builds dependency graph from component registry
2. Identifies leaves (components with no dependencies)
3. Generates data in topological order (dependencies first)
4. Creates references between components automatically
5. Uses GPT (if API key set) to generate realistic values

### Step 3: Use the Generated Data

The data is returned as JSON. You can:

**Option A: Store in Runtime (for standalone API)**
```python
from runtime import insert_account_component_record

for component_name, records in dataset.items():
    for record in records:
        insert_account_component_record(
            account_id="acct_123",
            component_name=component_name,
            payload=record
        )
```

**Option B: Store in Database (for main backend)**
```python
from reverse import runtime

runtime.replace_dataset("stripe", dataset)
```

## Python Usage

### Basic Example

```python
from reverse.data_synthesizer import synthesize_all_components

# Generate data for all components
data = synthesize_all_components(
    api_slug="stripe",
    count_per_component={
        "account": 5,
        "customer": 10,
        "charge": 20
    }
)

# Data is a dict: {component_name: [list of records]}
for component, records in data.items():
    print(f"{component}: {len(records)} records")
```

### Advanced Example

```python
from reverse.graph_based_generator import GraphDataGenerator

generator = GraphDataGenerator(api_slug="stripe")
# Reads OPENAI_API_KEY from environment automatically

# Generate data
data = generator.generate_all(
    count每_component={"account": 5, "customer": 10},
    seed_account_id="acct_123"  # For account-scoped storage
)

# Use the data
for component_name, records in data.items():
    print(f"Generated {len(records)} records for {component_name}")
    for record in records:
        print(f"  - {record.get('id')}: {record}")
```

## Integration with Existing Workflow

### Complete Pipeline

```bash
# 1. Upload spec
curl -X POST "http://localhost:8000/apis/upload" \
  -F "spec_file=@stripe_api.json"

# 2. Generate plan (automatic on upload)
curl -X POST "http://localhost:8000/reverse/plan" \
  -H "Content-Type: application/json" \
  -d '{"api_slug": "stripe"}'

# 3. Generate code
curl -X POST "http://localhost:8000/reverse/generate" \
  -H "Content-Type: application/json" \
  -d '{"api_slug": "stripe"}'

# 4. Generate data (NEW - for all components)
curl -X POST "http://localhost:8000/reverse/generate_data" \
  -H "Content-Type: application/json" \
  -d '{
    "api_slug": "stripe",
    "use_graph": true,
    "counts": {"account": 5, "customer": 10}
  }'

# 5. Apply to backend (optional)
curl -X POST "http://localhost:8000/reverse/apply" \
  -H "Content-Type: application/json" \
  -d '{"api_slug": "stripe"}'
```

## What Gets Generated

### With `use_graph: true` (NEW)

- **ALL components** in the component registry
- **Dependency-aware**: Generates in correct order
- **Reference integrity**: All foreign keys point to existing records
- **Realistic values**: Uses GPT if API key provided

**Example for Stripe:**
- Generates: `BalanceTransaction`, `Account`, `Customer`, `Charge`, `Subscription`, `PaymentIntent`, etc.
- All components, not just route components

### Without `use_graph` (Original)

- Only components referenced in routes
- Simple heuristic-based values
- May have broken references

## Real-World Example: Stripe API

```bash
# Set OpenAI key for realistic data
export OPENAI_API_KEY="sk-..."

# Generate comprehensive dataset
curl -X POST "http://localhost:8000/reverse/generate_data" \
  -H "Content-Type: application/json" \
  -d '{
    "api_slug": "stripe",
    "use_graph": true,
    "counts": {
      "balance_transaction": 10,
      "account": 3,
      "customer": 15,
      "charge": 30,
      "subscription": 10,
      "payment_intent": 25
    }
  }'
```

**Result:**
- ✅ All components have data
- ✅ References work (Charge → Customer → Account)
- ✅ Realistic values (emails like "john.doe@example.com" not "customer_0")
- ✅ Proper dependency order (BalanceTransaction before Account)

## For Standalone APIs

After generating data, populate the standalone API's runtime:

```python
# In generated_output/stripe/
from runtime import insert_account_component_record

# After calling generate_data API
dataset = {...}  # Response from API

# Store for each account
for component_name, records in dataset.items():
    for record in records:
        insert_account_component_record(
            account_id="acct_default",
            component_name=component_name,
            payload=record
        )
```

Or create a script:

```python
# seed_data.py in generated_output/stripe/
import requests
from runtime import insert_account_component_record

# Generate data
response = requests.post(
    "http://localhost:8000/reverse/generate_data",
    json={
        "api_slug": "stripe",
        "use_graph": True,
        "counts": {"account": 5, "customer": 10}
    }
)

dataset = response.json()["dataset"]

# Store in runtime
for component_name, records in dataset.items():
    for record in records:
        insert_account_component_record(
            account_id="acct_default",
            component_name=component_name,
            payload=record
        )

print("Data seeded!")
```

## Troubleshooting

**Q: No data generated?**
- Check `api_slug` matches your uploaded API
- Verify components exist: `curl http://localhost:8000/apis/stripe/components`

**Q: GPT not working?**
- Check `OPENAI_API_KEY` is set: `echo $OPENAI_API_KEY`
- Falls back to heuristics automatically if GPT fails

**Q: References broken?**
- Ensure `use_graph: true` (uses dependency graph)
- Check component graph: `curl http://localhost:8000/apis/stripe/graph`

**Q: Want more/less records?**
- Adjust `counts` object: `{"component": 10}` for 10 records

## Next Steps

1. Generate data: `use_graph: true` with your counts
2. Use data in your routes: Store in runtime or database
3. Test endpoints: Data will be available via your API
4. Customize: Edit `graph_based_generator.py` for custom field generators

See `GRAPH_DATA_GENERATION.md` for technical details.

