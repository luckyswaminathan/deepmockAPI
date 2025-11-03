# How to Use Your Existing Database with Docker Script

## The Problem

The script creates a **new empty database** by default. Your components are in your **existing database**.

## Solution: Export `_DATABASE_URL`

Before running the script, export your database URL:

```bash
export _DATABASE_URL="postgresql+psycopg://user:password@localhost:5432/deepmock"
```

Then run:
```bash
python3 backend/scripts/run_generation_job.py \
  --api-slug stripe \
  --manifest backend/reverse/generated/stripe/plan/plan.json \
  --output-dir ./generated_output
```

## Find Your Database URL

If you're running the backend locally, check:

```bash
# Check your environment
echo $_DATABASE_URL
echo $DATABASE_URL

# Or check your backend .env file
cat backend/.env | grep DATABASE
```

## Example

```bash
# Step 1: Export your database URL
export _DATABASE_URL="postgresql+psycopg://deepmock:deepmock@localhost:5432/deepmock"

# Step 2: Run generation
python3 backend/scripts/run_generation_job.py \
  --api-slug stripe \
  --manifest backend/reverse/generated/stripe/plan/plan.json \
  --output-dir ./generated_output
```

The script will:
1. Detect `_DATABASE_URL` from environment
2. Convert `localhost` → `host.docker.internal` (so Docker can reach it)
3. Connect to your existing database
4. Find your existing components
5. Generate data successfully!

## Verify It's Working

You should see in the output:
```
[run_generation_job] Found database URL in environment: _DATABASE_URL
[run_generation_job] Updated database URL to use host.docker.internal for Docker networking
[run_generation_job] Using existing database: host.docker.internal:5432/deepmock
[synthesize_all_components] Checking components for 'stripe' using database: host.docker.internal:5432/devmock
[synthesize_all_components] Found X components for 'stripe'
[construct_component_graph] ComponentRegistry contains X total records
```

If you see `Found 0 components`, it means:
- Either `_DATABASE_URL` isn't set (script is using transient DB)
- Or the database connection isn't working

Make sure to **export `_DATABASE_URL`** before running the script!

