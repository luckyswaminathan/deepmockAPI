import os
from contextlib import contextmanager
from functools import lru_cache

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    MetaData,
    String,
    Table,
    UniqueConstraint,
    create_engine,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.engine import Engine


import os
from dotenv import load_dotenv

load_dotenv()

@lru_cache(maxsize=1)
def get_database_url() -> str:
    url = os.getenv("_DATABASE_URL")
    if not url:
        raise RuntimeError(
            "DATABASE_URL environment variable is required (e.g., "
            "'postgresql+psycopg://user:password@localhost:5432/deepmock')."
        )
    return url


@lru_cache(maxsize=1)
def get_engine() -> Engine:
    url = get_database_url()
    return create_engine(
        url,
        future=True,
        pool_pre_ping=True,
    )


metadata = MetaData()

api_registry = Table(
    "api_registry",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("api_slug", String(100), nullable=False, unique=True),
    Column("api_name", String(200), nullable=False),
    Column("title", String(255), nullable=False),
    Column("version", String(50), nullable=True),
    Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False),
)

component_registry = Table(
    "component_registry",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("api_slug", String(100), nullable=False),
    Column("component_name", String(200), nullable=False),
    Column("table_name", String(255), nullable=False),
    Column("schema", JSONB, nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False),
    UniqueConstraint("api_slug", "component_name", name="uq_component_registry_slug_component"),
)


def init_core_tables() -> None:
    """Create registry tables if they do not already exist."""
    engine = get_engine()
    metadata.create_all(engine, tables=[api_registry, component_registry])


@contextmanager
def db_connection():
    """Provide a transactional scope around a series of operations."""
    engine = get_engine()
    with engine.begin() as conn:
        yield conn
