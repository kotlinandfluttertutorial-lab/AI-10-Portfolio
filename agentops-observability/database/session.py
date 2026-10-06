"""Database session factory and Redis client initialisation.

The session factory is created lazily on first use so that the module can
be imported in tests without a live database connection.
"""

from functools import lru_cache

import redis.asyncio as aioredis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from api.config import get_settings


class Base(DeclarativeBase):
    """SQLAlchemy declarative base shared by all ORM models."""


@lru_cache
def _get_engine() -> object:
    settings = get_settings()
    return create_async_engine(
        settings.database_url,
        echo=False,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
    )


@lru_cache
def _get_session_factory() -> async_sessionmaker[AsyncSession]:
    engine = _get_engine()
    return async_sessionmaker(  # type: ignore[call-overload]
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )


def AsyncSessionLocal() -> AsyncSession:  # noqa: N802  (uppercase matches SQLAlchemy convention)
    """Return a new async database session."""
    return _get_session_factory()()


@lru_cache
def get_redis_client() -> aioredis.Redis:  # type: ignore[type-arg]
    """Return a shared async Redis client (one per process)."""
    settings = get_settings()
    return aioredis.from_url(settings.redis_url, decode_responses=True)
