FROM postgres:16-alpine

# ── Variables de entorno para inicializar la BD ──────────────
ENV POSTGRES_DB=notesdb
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres

# ── Scripts de inicialización ────────────────────────────────
# PostgreSQL ejecuta automáticamente todos los .sql de esta
# carpeta en orden alfabético la primera vez que arranca.
COPY init/ /docker-entrypoint-initdb.d/

EXPOSE 5432
