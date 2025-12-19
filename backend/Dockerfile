FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install system dependencies required for psycopg and build tooling.
# RUN apt-get update \
#     && apt-get install --yes --no-install-recommends build-essential libpq-dev curl \
#     && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY backend/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip \
    && pip install -r /app/requirements.txt

COPY . /app

# Install the backend package in editable mode so local changes are reflected.
RUN pip install -e /app/backend

ENV PYTHONPATH=/app/backend:/app

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
