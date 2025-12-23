import os
from contextlib import contextmanager
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterator, Optional

from dotenv import load_dotenv
from sqlalchemy import Column, DateTime, Integer, String, TypeDecorator, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.engine import Engine, make_url
from sqlalchemy.types import JSON, TypeEngine
from sqlmodel import Field, Session, SQLModel, create_engine


load_dotenv()


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_SQLITE_PATH = (BASE_DIR / "deepmock.db").resolve()


def _env_database_url() -> Optional[str]:
    return os.getenv("_DATABASE_URL") or os.getenv("DATABASE_URL")


def _default_sqlite_url() -> str:
    return f"sqlite:///{DEFAULT_SQLITE_PATH}"


def _normalize_sqlite_url(url: str) -> str:
    try:
        parsed = make_url(url)
    except Exception:
        return url

    database = parsed.database
    if not database or database == ":memory:":
        return url

    db_path = Path(database)
    if not db_path.is_absolute():
        db_path = (BASE_DIR / db_path).resolve()

    return f"sqlite:///{db_path}"


class AdaptiveJSON(TypeDecorator):
    """JSON type that adapts to SQLite (JSON) or PostgreSQL (JSONB) at runtime."""
    
    impl = JSON
    cache_ok = True
    
    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(JSONB())
        else:
            return dialect.type_descriptor(JSON())


def _schema_type() -> Any:
    """Return appropriate JSON type based on database dialect.
    
    Returns AdaptiveJSON which will use JSON for SQLite and JSONB for PostgreSQL
    based on the actual database dialect at table creation time.
    """
    return AdaptiveJSON()


class ApiRegistry(SQLModel, table=True):
    __tablename__ = "api_registry"
    __table_args__ = {"extend_existing": True}

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
        {"extend_existing": True},
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    api_slug: str = Field(sa_column=Column(String(100), nullable=False))
    component_name: str = Field(sa_column=Column(String(200), nullable=False))
    table_name: str = Field(sa_column=Column(String(255), nullable=False))
    schema_payload: dict[str, Any] = Field(sa_column=Column("schema", _schema_type(), nullable=False))
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False),
    )


class GeneratedRecord(SQLModel, table=True):
    __tablename__ = "generated_records"
    __table_args__ = (
        UniqueConstraint(
            "api_slug",
            "component_name",
            "record_key",
            name="uq_generated_records_slug_component_key",
        ),
        {"extend_existing": True},
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    api_slug: str = Field(sa_column=Column(String(100), nullable=False))
    component_name: str = Field(sa_column=Column(String(200), nullable=False))
    record_key: str = Field(sa_column=Column(String(255), nullable=False))
    payload: dict[str, Any] = Field(sa_column=Column(_schema_type(), nullable=False))
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False),
    )


class RLStateRecord(SQLModel, table=True):
    __tablename__ = "rl_states"
    __table_args__ = {"extend_existing": True}

    state_id: str = Field(sa_column=Column(String(100), primary_key=True, nullable=False))
    api_slug: str = Field(sa_column=Column(String(100), nullable=False, index=False))  # Index created separately if needed
    parent_state_id: Optional[str] = Field(
        default=None,
        sa_column=Column(String(100), nullable=True, index=False),  # Index created separately if needed
    )
    action_path: list[str] = Field(
        default_factory=list,
        sa_column=Column(_schema_type(), nullable=False),
    )
    modified_components: dict[str, Any] = Field(
        default_factory=dict,
        sa_column=Column(_schema_type(), nullable=False),
    )
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False),
    )


@lru_cache(maxsize=1)
def get_database_url() -> str:
    url = _env_database_url()
    if url:
        if url.startswith("sqlite"):
            return _normalize_sqlite_url(url)
        return url
    return _default_sqlite_url()


@lru_cache(maxsize=1)
def get_engine() -> Engine:
    url = get_database_url()
    engine_kwargs: dict[str, Any] = {
        "future": True,
        "pool_pre_ping": True,
    }
    if url.startswith("sqlite"):
        # Ensure the SQLite directory exists before connecting
        try:
            parsed = make_url(url)
            database = parsed.database
        except Exception:
            database = None

        if database and database != ":memory:":
            db_path = Path(database)
            db_path.parent.mkdir(parents=True, exist_ok=True)
        engine_kwargs["connect_args"] = {"check_same_thread": False}

    return create_engine(
        url,
        **engine_kwargs,
    )


def init_core_tables() -> None:
    """Create registry tables if they do not already exist."""
    import sys
    try:
        engine = get_engine()
        # Use checkfirst=True to avoid errors if tables/indexes already exist
        SQLModel.metadata.create_all(engine, checkfirst=True)
        
        # Create indexes separately if they don't exist (for RLStateRecord)
        # This avoids duplicate index errors during hot reload
        from sqlalchemy import Index, inspect
        inspector = inspect(engine)
        
        # Check and create indexes for rl_states table if needed
        if inspector.has_table("rl_states"):
            existing_indexes = {idx["name"] for idx in inspector.get_indexes("rl_states")}
            
            # Create api_slug index if it doesn't exist
            if "ix_rl_states_api_slug" not in existing_indexes:
                try:
                    Index("ix_rl_states_api_slug", RLStateRecord.api_slug).create(engine, checkfirst=True)
                except Exception:
                    pass  # Index might already exist, ignore
            
            # Create parent_state_id index if it doesn't exist
            if "ix_rl_states_parent_state_id" not in existing_indexes:
                try:
                    Index("ix_rl_states_parent_state_id", RLStateRecord.parent_state_id).create(engine, checkfirst=True)
                except Exception:
                    pass  # Index might already exist, ignore
        
        print("[database] Core tables initialized successfully", file=sys.stderr)
    except Exception as e:
        import traceback
        print(f"[database] ERROR: Failed to create tables: {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        raise


@contextmanager
def db_session() -> Iterator[Session]:
    """Provide a transactional SQLModel session."""
    engine = get_engine()
    with Session(engine, expire_on_commit=False) as session:
        with session.begin():
            yield session
