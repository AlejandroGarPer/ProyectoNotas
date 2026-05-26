"""
Servicio de notas.
Aquí vive la lógica de negocio: validaciones, reglas, orquestación.
Los servicios llaman al repositorio; nunca hablan directamente con la BD.
"""
from ..repositories import notes_repository
from ..models.note import Note


def list_notes() -> list[Note]:
    """Devuelve todas las notas."""
    return notes_repository.get_all()


def get_note(note_id: int) -> tuple[Note | None, str | None]:
    """
    Devuelve (nota, None) si existe o (None, mensaje_error) si no.
    """
    note = notes_repository.get_by_id(note_id)
    if not note:
        return None, "Nota no encontrada"
    return note, None


def create_note(name: str, content: str) -> tuple[Note | None, str | None]:
    """
    Crea una nota nueva.
    Devuelve (nota, None) o (None, mensaje_error).
    """
    name = name.strip()
    if not name:
        return None, "El nombre de la nota es requerido"
    if notes_repository.get_by_name(name):
        return None, "Ya existe una nota con ese nombre"

    note = notes_repository.create(name, content)
    return note, None


def update_note(
    note_id: int,
    name: str | None = None,
    content: str | None = None,
) -> tuple[Note | None, str | None]:
    """
    Actualiza una nota existente.
    Devuelve (nota_actualizada, None) o (None, mensaje_error).
    """
    existing = notes_repository.get_by_id(note_id)
    if not existing:
        return None, "Nota no encontrada"

    new_name: str | None = name.strip() if name else None

    # Validar nombre duplicado solo si cambia
    if new_name and new_name != existing.name:
        if notes_repository.get_by_name(new_name):
            return None, "Ya existe una nota con ese nombre"
    else:
        new_name = None  # No hay cambio real de nombre

    note = notes_repository.update(note_id, name=new_name, content=content)
    return note, None


def delete_note(note_id: int) -> tuple[bool, str | None]:
    """
    Elimina una nota.
    Devuelve (True, None) si se eliminó o (False, mensaje_error) si no existía.
    """
    if not notes_repository.get_by_id(note_id):
        return False, "Nota no encontrada"
    notes_repository.delete(note_id)
    return True, None
