# Fix: Docker Script Uses Empty Database

## The Problem

When you run:
```bash
python3 backend/scripts/run_generation_job.py --api-slug stripe ...
```

The script creates a **NEW, empty PostgreSQL container** with database `deepmock_stripe`. This database:
- ✅ Has tables created
- ❌ Is **completely empty** (no components!)

Your main database has:
- ✅ `api_registry` with stripe
- ✅ `component_registry` with all stripe components

But the Docker container uses a **different, empty database**!

## Solution: Use Your Existing Database

Use `--shared-database-url` to point to your main database:

```bash
python3 backend/scripts/run_generation_job.py \
  --api-slug stripe \
  --manifest backend/reverse/generated/stripe/plan/plan.json \
  --output-dir ./generated_output \
  --shared-database-url "postgresql+psycopg://user:password@host:5432/deepmock"
```

Replace with your actual database connection string:
- `user`: Your PostgreSQL user
- `password`: Your password  
- `host`: `localhost` if local, or your DB host
- `deepmock`: Your database name

## How to Find Your Database URL

1. **Check your environment:**
   ```bash
   echo $DATABASE_URL
   # or
   echo $_DATABASE_URL
   ```

2. **Or from your backend .env file:**
   ```bash
   cat backend/.env | grep DATABASE
   ```

3. **Format should be:**
   ```
   postgresql+psycopg://user:password@localhost:5432/deepmock
   ```

## Example

```bash
python3 backend/scripts/run_generation_job.py \
  --api-slug stripe \
  --manifest backend/reverse/generated/stripe/plan/plan.json \
  --output-dir ./generated_output \
  --shared-database-url "postgresql+psycopg://deepmock:deepmock@localhost:5432/deepmock"
```

Now it will use your existing database with all the components!

