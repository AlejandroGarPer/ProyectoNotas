"""
Endpoints REST para el recurso /notes.
Cada ruta delega la lógica al servicio correspondiente.
"""
from flask import Blueprint, request, jsonify
from .services import notes_service

notes_bp = Blueprint("notes", __name__, url_prefix="/notes")


# ──────────────────────────────────────────────
# GET /notes  →  Listar todas las notas
# ──────────────────────────────────────────────
@notes_bp.route("", methods=["GET"])
def list_notes():
    notes = notes_service.list_notes()
    return jsonify([note.to_dict() for note in notes])


# ──────────────────────────────────────────────
# POST /notes  →  Crear una nota nueva
# ──────────────────────────────────────────────
@notes_bp.route("", methods=["POST"])
def create_note():
    data = request.get_json() or {}
    note, error = notes_service.create_note(
        name=data.get("name", ""),
        content=data.get("content", ""),
    )
    if error:
        status = 409 if "existe" in error else 400
        return jsonify({"error": error}), status
    return jsonify({"message": "Nota creada", "note": note.to_dict()}), 201


# ──────────────────────────────────────────────
# GET /notes/<id>  →  Obtener una nota por ID
# ──────────────────────────────────────────────
@notes_bp.route("/<int:note_id>", methods=["GET"])
def get_note(note_id: int):
    note, error = notes_service.get_note(note_id)
    if error:
        return jsonify({"error": error}), 404
    return jsonify(note.to_dict())


# ──────────────────────────────────────────────
# PUT /notes/<id>  →  Actualizar nombre y/o contenido
# ──────────────────────────────────────────────
@notes_bp.route("/<int:note_id>", methods=["PUT"])
def update_note(note_id: int):
    data = request.get_json() or {}
    note, error = notes_service.update_note(
        note_id=note_id,
        name=data.get("name"),
        content=data.get("content"),
    )
    if error:
        status = 404 if "encontrada" in error else 409
        return jsonify({"error": error}), status
    return jsonify({"message": "Nota actualizada", "note": note.to_dict()})


# ──────────────────────────────────────────────
# DELETE /notes/<id>  →  Eliminar una nota
# ──────────────────────────────────────────────
@notes_bp.route("/<int:note_id>", methods=["DELETE"])
def delete_note(note_id: int):
    success, error = notes_service.delete_note(note_id)
    if error:
        return jsonify({"error": error}), 404
    return jsonify({"message": "Nota eliminada"})
