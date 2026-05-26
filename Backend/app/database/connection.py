import psycopg2
import psycopg2.pool
from contextlib import contextmanager
from ..config import Config

_pool: psycopg2.pool.SimpleConnectionPool | None = None


def init_pool() -> None:
    """Inicializa el pool de conexiones a PostgreSQL."""
    global _pool
    _pool = psycopg2.pool.SimpleConnectionPool(
        minconn=1,
        maxconn=10,
        dsn=Config.DATABASE_URL,
    )


@contextmanager
def get_db():
    """
    Context manager que entrega una conexión del pool y gestiona
    commit / rollback automáticamente.

    Uso:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute(...)
    """
    if _pool is None:
        raise RuntimeError("El pool de conexiones no ha sido inicializado. Llama a init_pool() primero.")

    conn = _pool.getconn()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        _pool.putconn(conn)
