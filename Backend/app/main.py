"""
Punto de entrada de la aplicación Flask.

Para ejecutar (desde la carpeta Backend/):
    python -m app.main
    -- o --
    flask --app app.main run --debug
"""
from flask import Flask, jsonify
from flask_cors import CORS

from .config import Config
from .database.connection import init_pool
from .api.notes import notes_bp


def create_app() -> Flask:
    """Factory que crea y configura la aplicación Flask."""
    app = Flask(__name__)

    # Configuración
    app.config["DEBUG"] = Config.DEBUG

    # CORS — permite peticiones desde el frontend
    CORS(app)

    # Pool de conexiones a PostgreSQL
    init_pool()

    # Registrar blueprints (rutas)
    app.register_blueprint(notes_bp)

    # ── Health check ──────────────────────────────────────────
    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok"})

    return app


# ── Arranque directo ──────────────────────────────────────────
if __name__ == "__main__":
    app = create_app()
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
