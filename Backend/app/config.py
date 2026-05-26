import os
from dotenv import load_dotenv

load_dotenv()

# Dentro de Docker, "localhost" apunta al propio contenedor.
# host.docker.internal resuelve al localhost de la máquina Windows.
_default_db = "postgresql://postgres:postgres@host.docker.internal:5432/notesdb"


class Config:
    DATABASE_URL: str = os.environ.get("DATABASE_URL", _default_db)
    DEBUG: bool = os.environ.get("DEBUG", "false").lower() == "true"
    HOST: str = os.environ.get("HOST", "0.0.0.0")
    PORT: int = int(os.environ.get("PORT", 5000))
