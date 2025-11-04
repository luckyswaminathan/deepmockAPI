"""Standalone FastAPI application for Stripe API mock."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from code.routes import router

app = FastAPI(
    title="Stripe API Mock",
    description="Generated mock API for Stripe",
    version="1.0.0",
)

# CORS: allow all origins for a standalone mock API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the generated routes
app.include_router(router)

# Load generated seed data on startup
@app.on_event("startup")
async def load_seed_data() -> None:
    """Load generated seed data into runtime storage."""
    try:
        import json
        from pathlib import Path
        
        seed_file = Path(__file__).parent / "data" / "seeds" / "generated.json"
        if seed_file.exists():
            with open(seed_file) as f:
                seed_data = json.load(f)
            
            dataset = seed_data.get("dataset", {})
            
            # Import runtime
            import runtime
            
            # Load into runtime storage
            for component_name, records in dataset.items():
                for record in records:
                    runtime.insert_component_record("stripe", component_name, record)
            
            # Distribute account-scoped components (like balance) to each mock account
            # Get all mock account IDs from auth module if it exists
            account_scoped_components = ["balance", "balance_transaction"]
            mock_accounts = []
            
            try:
                # Try to get mock accounts from auth module (if it exists)
                from auth import _MOCK_API_KEYS
                mock_accounts = [
                    info.get("account_id") 
                    for info in _MOCK_API_KEYS.values() 
                    if info.get("account_id")
                ]
            except (ImportError, AttributeError, KeyError):
                # Auth module doesn't exist or doesn't have expected structure - use default accounts
                mock_accounts = ["acct_default", "acct_123456", "acct_production"]
            
            # Distribute account-scoped data to each account
            # Give each account at least one record (round-robin if multiple records exist)
            for component_name in account_scoped_components:
                if component_name in dataset:
                    component_records = dataset[component_name]
                    for idx, account_id in enumerate(mock_accounts):
                        if component_records:
                            record_index = idx % len(component_records)
                            record = component_records[record_index].copy()
                            runtime.insert_account_component_record(
                                account_id, component_name, record
                            )
            
            total_records = sum(len(records) for records in dataset.values())
            account_records = sum(
                len(records) 
                for component in account_scoped_components 
                if component in dataset 
                for records in [dataset[component]] 
                for _ in mock_accounts
            )
            print(f"Loaded {total_records} records into runtime storage")
            if account_records > 0:
                print(f"Distributed {account_records} account-scoped records to {len(mock_accounts)} accounts")
    except Exception as e:
        print(f"Warning: Could not load seed data: {e}")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "stripe-api-mock"}


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
