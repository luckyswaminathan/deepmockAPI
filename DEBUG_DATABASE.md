# Debugging Database Storage Issue

## Check Database Connection

1. **Check if DATABASE_URL is set:**
   ```bash
   echo $DATABASE_URL
   # or
   echo $_DATABASE_URL
   ```

2. **Check database directly:**
   ```bash
   psql -U your_user -d deepmock -c "SELECT COUNT(*) FROM generated_records;"
   ```

## Running Generation with Debug Output

When you run generation, you should now see detailed logs:

```
[generator] Starting data generation for stripe...
[generator] Generated dataset with X components
[generator] Storing Y total records in database...
[runtime.replace_dataset] Starting store for stripe with X components
[runtime.replace_dataset] Cleared existing records for stripe
[runtime.replace_dataset] Added 3 records for component 'account'
[runtime.replace_dataset] Added 3 records for component 'customer'
...
[runtime.replace_dataset] Successfully stored Y total records for stripe
[generator] Successfully stored Y records for stripe
```

## Common Issues

1. **DATABASE_URL not set**
   - Error: "DATABASE_URL environment variable is required"
   - Fix: `export DATABASE_URL="postgresql+psycopg://user:password@localhost:5432/deepmock"`

2. **Database not initialized**
   - Error: Table doesn't exist
   - Fix: Make sure `init_core_tables()` runs (happens automatically in FastAPI app)

3. **Empty dataset**
   - Check logs for: "WARNING: Dataset is empty"
   - Means data generation is failing silently

4. **Database connection fails**
   - Check PostgreSQL is running
   - Check connection string is correct

## Test Data Generation Directly

```python
from backend.reverse import data_synthesizer, runtime

# Generate data
dataset = data_synthesizer.synthesize_all_components("stripe", store_in_db=False)

# Check what was generated
print(f"Components: {len(dataset)}")
for comp, records in dataset.items():
    print(f"  {comp}: {len(records)} records")

# Store it
if dataset:
    runtime.replace_dataset("stripe", dataset)
```

## Verify Storage

```python
from backend.reverse import runtime
from backend.database import db_session, GeneratedRecord
from sqlmodel import select

# Check via runtime
records = runtime.fetch_component_records("stripe", "account")
print(f"Account records: {len(records)}")

# Check via direct DB query
with db_session() as session:
    all_records = session.exec(select(GeneratedRecord).where(GeneratedRecord.api_slug == "stripe")).all()
    print(f"Total records in DB: {len(all_records)}")
```

