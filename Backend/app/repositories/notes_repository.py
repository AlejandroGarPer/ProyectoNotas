"""
Repositorio de notas.
Toda la comunicación con la base de datos pasa por aquí mediante SQL puro.
"""
from ..database.connection import get_db
from ..models.note import Note


_SELECT = "SELECT id, name, content, created_at, updated_at FROM notes"


def get_all() -> list[Note]:
    """Devuelve todas las notas ordenadas por última modificación."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(f"{_SELECT} ORDER BY updated_at DESC")
            return [Note.from_row(row) for row in cur.fetchall()]


def get_by_id(note_id: int) -> Note | None:
    """Devuelve una nota por su ID o None si no existe."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(f"{_SELECT} WHERE id = %s", (note_id,))
            row = cur.fetchone()
            return Note.from_row(row) if row else None


def get_by_name(name: str) -> Note | None:
    """Devuelve una nota por su nombre o None si no existe."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(f"{_SELECT} WHERE name = %s", (name,))
            row = cur.fetchone()
            return Note.from_row(row) if row else None


def create(name: str, content: str) -> Note:
    """Inserta una nueva nota y devuelve el registro creado."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                INSERT INTO notes (name, content)
                VALUES (%s, %s)
                RETURNING id, name, content, created_at, updated_at
                """,
                (name, content),
            )
            return Note.from_row(cur.fetchone())


def update(note_id: int, name: str | None = None, content: str | None = None) -> Note | None:
    """Actualiza los campos indicados de una nota y devuelve el registro actualizado."""
    fields: list[str] = []
    values: list = []

    if name is not None:
        fields.append("name = %s")
        values.append(name)
    if content is not None:
        fields.append("content = %s")
        values.append(content)

    if not fields:
        return get_by_id(note_id)

    values.append(note_id)
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                UPDATE notes
                SET {", ".join(fields)}
                WHERE id = %s
                RETURNING id, name, content, created_at, updated_at
                """,
                values,
            )
            row = cur.fetchone()
            return Note.from_row(row) if row else None


def delete(note_id: int) -> bool:
    """Elimina una nota. Devuelve True si existía, False si no."""
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM notes WHERE id = %s RETURNING id", (note_id,))
            return cur.fetchone() is not None
