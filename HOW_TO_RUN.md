# How to Run Generation - Quick Guide

## Two Simple Steps

### Step 1: Upload Your OpenAPI Spec

```bash
curl -X POST "http://localhost:8000/apis/upload" \
  -F "spec_file=@path/to/openapi.json" \
  -F "api_name=Your API"
```

**Or use web UI:** `http://localhost:3000/upload`

**You'll get back:** `{"api_slug": "your_api", ...}`

### Step 2: Generate Everything (One Command!)

```bash
curl -X POST "http://localhost:8000/reverse/apply" \
  -H "Content-Type: application/json" \
  -d '{"api_slug": "your_api"}'
```

**This automatically:**
- ✅ Generates code (routes, tests)
- ✅ Generates data for ALL components (using dependency graph)
- ✅ Creates standalone API in `generated_output/your_api/`
- ✅ Seeds data ready to use

### Step 3: Run Your Standalone API

```bash
cd generated_output/your_api
pip install -r requirements.txt
python main.py
```

Data is automatically loaded on startup!

## Complete Example

```bash
# 1. Upload
curl -X POST "http://localhost:8000/apis/upload" \
  -F "spec_file=@backend/schemas/stripe_api.json" \
  -F "api_name=Stripe"

# 2. Generate (this does EVERYTHING)
curl -X POST "http://localhost:8000/reverse/apply" \
  -H "Content-Type: application/json" \
  -d '{"api_slug": "stripe"}'

# 3. Run
cd generated_output/stripe
pip install -r requirements.txt
python main.py

# 4. Test
curl http://localhost:8000/v1/accounts
# Open http://localhost:8000/docs for interactive docs
```

## What Gets Created

```
generated_output/your_api/
├── main.py              # ← Run this: python main.py
├── runtime.py           # In-memory storage
├── requirements.txt     # Dependencies
├── code/
│   └── routes.py       # All your routes
├── data/
│   └── seeds/
│       └── generated.json  # Pre-generated data (auto-loaded)
└── plan/
    └── plan.json       # Generation plan
```

## Optional: Customize Data Generation

Want more records per component?

```bash
curl -X POST "http://localhost:8000/reverse/generate_data" \
  -H "Content-Type: application/json" \
  -d '{
    "api_slug": "your_api",
    "use_graph": true,
    "counts": {
      "account": 10,
      "customer": 20
    }
  }'
```

Then update `generated_output/your_api/data/seeds/generated.json` or regenerate.

## Troubleshooting

**Backend not running?**
```bash
cd backend
export DATABASE_URL='postgresql+psycopg://user:pass@localhost:5432/deepmock'
python main.py
```

**Import errors?** 
- The sync process now automatically fixes imports in `routes.py`
- If issues persist, check `runtime.py` exists in `generated_output/your_api/`

**No data?**
- Check `data/seeds/generated.json` exists
- Check startup logs for "Loaded X records"

That's it! Just two API calls and you have a fully functional standalone mock API with data. 🚀

