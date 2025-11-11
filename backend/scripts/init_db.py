#!/usr/bin/env python3
"""Script to initialize database tables."""

import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from database import init_core_tables

if __name__ == "__main__":
    try:
        print("Initializing database tables...")
        init_core_tables()
        print("✅ Database tables initialized successfully!")
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

