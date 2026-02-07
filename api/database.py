"""
Database connection setup using SQLAlchemy.

Compatible with Supabase PostgreSQL on the free tier.
Uses connection pooling with pre-ping to handle
intermittent connection drops common on free-tier databases.
"""
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from api.config import settings

logger = logging.getLogger(__name__)

# SQLite needs check_same_thread=False for FastAPI's async/threading model
_engine_kwargs = {"pool_pre_ping": True}
if settings.database_url.startswith("sqlite"):
    _engine_kwargs["connect_args"] = {"check_same_thread": False}
    _engine_kwargs["pool_pre_ping"] = False  # not used for SQLite

engine = create_engine(settings.database_url, **_engine_kwargs)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    FastAPI dependency that provides a database session per request.
    Ensures sessions are properly closed after use to prevent
    connection leaks.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Create all database tables on startup.
    Safe to call multiple times - SQLAlchemy only creates
    tables that don't already exist.
    """
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables initialized successfully")
