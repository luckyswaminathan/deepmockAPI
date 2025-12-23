"""Load generated seed data into runtime storage.

This script loads the generated data from data/seeds/generated.json into
the runtime storage so it's available when the API starts.
"""

import json
from pathlib import Path

# Import runtime (will work when run from generated_output/sample_api/)
import sys
sys.path.insert(0, str(Path(__file__).parent))

try:
    import runtime
    
    seed_file = Path(__file__).parent / "data" / "seeds" / "generated.json"
    if seed_file.exists():
        with open(seed_file) as f:
            seed_data = json.load(f)
        
        dataset = seed_data.get("dataset", {})
        
        # Load into runtime storage
        for component_name, records in dataset.items():
            for record in records:
                runtime.insert_component_record("sample_api", component_name, record)
        
        total_records = sum(len(records) for records in dataset.values())
        print(f"Loaded {total_records} records into runtime storage")
    else:
        print(f"Seed file not found: {seed_file}")
except Exception as e:
    print(f"Warning: Could not load seed data: {e}")
