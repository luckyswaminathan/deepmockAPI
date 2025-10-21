import os
from contextlib import contextmanager
from datetime import datetime
from functools import lru_cache
from typing import Any, Iterator, Optional

from dotenv import load_dotenv
from sqlalchemy import Column, DateTime, Integer, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.engine import Engine
from sqlmodel import Field, Session, SQLModel, create_engine


load_dotenv()


class ApiRegistry(SQLModel, table=True):
    __tablename__ = "api_registry"

    id: Optional[int] = Field(default=None, primary_key=True)
    api_slug: str = Field(sa_column=Column(String(100), nullable=False, unique=True))
    api_name: str = Field(sa_column=Column(String(200), nullable=False))
    title: str = Field(sa_column=Column(String(255), nullable=False))
    version: Optional[str] = Field(default=None, sa_column=Column(String(50)))
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False),
    )


class ComponentRegistry(SQLModel, table=True):
    __tablename__ = "component_registry"
    __table_args__ = (
        UniqueConstraint("api_slug", "component_name", name="uq_component_registry_slug_component"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    api_slug: str = Field(sa_column=Column(String(100), nullable=False))
    component_name: str = Field(sa_column=Column(String(200), nullable=False))
    table_name: str = Field(sa_column=Column(String(255), nullable=False))
    schema: dict[str, Any] = Field(sa_column=Column(JSONB, nullable=False))
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False),
    )


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


def init_core_tables() -> None:
    """Create registry tables if they do not already exist."""
    engine = get_engine()
    SQLModel.metadata.create_all(engine)


@contextmanager
def db_session() -> Iterator[Session]:
    """Provide a transactional SQLModel session."""
    engine = get_engine()
    with Session(engine, expire_on_commit=False) as session:
        with session.begin():
            yield session
