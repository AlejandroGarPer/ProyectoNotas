from dataclasses import dataclass
from datetime import datetime


@dataclass
class Note:
    """
    Representación Python de una fila de la tabla 'notes'.
    No es un modelo ORM: la estructura real está en database/schema.sql.
    """
    id: int
    name: str
    content: str
    created_at: datetime
    updated_at: datetime

    # ── Serialización ──────────────────────────────────────────
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "content": self.content,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    # ── Construcción desde fila de psycopg2 ────────────────────
    @staticmethod
    def from_row(row: tuple) -> "Note":
        """Crea un Note a partir de una tupla devuelta por psycopg2."""
        return Note(
            id=row[0],
            name=row[1],
            content=row[2],
            created_at=row[3],
            updated_at=row[4],
        )
