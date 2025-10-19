FastAPI Backend
===============

Prerequisites
-------------
- Python 3.12+

Setup
-----
1. Create a virtual environment (recommended)
   
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies
   
   ```bash
   pip install -r requirements.txt
   ```

Run
---
- Start the development server with reload:
  
  ```bash
  python backend/main.py
  ```

- Or run via Uvicorn directly:
  
  ```bash
  uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
  ```

Visit
-----
- API root: `http://localhost:8000/`
- Interactive docs (Swagger): `http://localhost:8000/docs`
- Alternative docs (ReDoc): `http://localhost:8000/redoc`

