from sqlite3 import connect

from sqlalchemy import Column, DateTime, create_engine, func

from core.singleton import SingletonWrapper


def init_postgres(
    username: str,
    password: str,
    host: str,
    port: int,
    db: str,
    pool_size: int = 5,
    max_overflow: int = 10,
):
    """Initialize Postgres connection."""
    return create_engine(
        f"postgresql://{username}:{password}@{host}:{port}/{db}",
        pool_size=pool_size,
        max_overflow=max_overflow,
    ).connect()


def establish_postgres_connection(
    username: str,
    password: str,
    host: str,
    port: int,
    db: str,
    pool_size: int = 5,
    max_overflow: int = 10,
):
    """Establish Postgres connection."""
    return init_postgres(
        username=username,
        password=password,
        host=host,
        port=port,
        db=db,
        pool_size=pool_size,
        max_overflow=max_overflow,
    )
