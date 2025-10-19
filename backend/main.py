from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"status": "ok", "message": "DeepMock API is running"}


if __name__ == "__main__":
    # Enable local development with: python backend/main.py
    import uvicorn

    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
