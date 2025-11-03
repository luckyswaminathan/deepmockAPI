# Data Generation Flow

## Where Data Generation Happens

### ✅ `/reverse/generate` - **YES, Automatic**
When you generate the API code, data is **automatically** generated:

```bash
POST /reverse/generate {"api_slug": "stripe"}
```

**What happens:**
1. Generates code (routes, tests)
2. **Automatically generates data** for ALL components ✨
3. Stores data in `generated_records` table

### ✅ `/reverse/apply` - **YES, Automatic**
When you apply the generated API, data is also automatically generated:

```bash
POST /reverse/apply {"api_slug": "stripe"}
```

**What happens:**
1. Generates code (routes, tests)
2. **Automatically generates data** for ALL components ✨
3. Stores data in `generated_records` table
4. Syncs to `generated_output/` (standalone API)
5. Mounts routes in main backend

### ❌ `/apis/upload` - **NO**
Upload only ingests the spec - no code or data generation:

```bash
POST /apis/upload
```

**What happens:**
1. Ingests OpenAPI spec
2. Stores components in database
3. Creates a plan (optional)
4. **NO code generation**
5. **NO data generation**

## Complete Pipeline

```
1. Upload Spec
   POST /apis/upload
   → Only ingests spec, stores components
   
2. Generate API (Choose One)
   
   Option A: Generate
   POST /reverse/generate
   → Generates code + data automatically ✅
   
   Option B: Apply (Full Pipeline)
   POST /reverse/apply
   → Generates code + data + syncs + mounts ✅
   
3. Run Standalone API
   cd generated_output/stripe
   python main.py
   → Data already loaded from generation!
```

## Summary

**Data generation happens on:**
- ✅ `/reverse/generate` - When generating code
- ✅ `/reverse/apply` - When applying to backend

**Data generation does NOT happen on:**
- ❌ `/apis/upload` - Only ingests spec

So when you call **either `/reverse/generate` OR `/reverse/apply`**, data is automatically generated for ALL components and stored in the `generated_records` table. No separate data generation step needed!

