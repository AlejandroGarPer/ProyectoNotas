-- ============================================================
-- Schema de la base de datos: notesdb
-- Ejecutar este archivo una sola vez para crear las tablas.
-- ============================================================

-- Tabla principal de notas
CREATE TABLE IF NOT EXISTS notes (
    id         SERIAL                   PRIMARY KEY,
    name       VARCHAR(255)             NOT NULL UNIQUE,
    content    TEXT                     NOT NULL DEFAULT '',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ──────────────────────────────────────────────────────────
-- Trigger para actualizar updated_at automáticamente
-- ──────────────────────────────────────────────────────────

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS set_updated_at ON notes;

CREATE TRIGGER set_updated_at
    BEFORE UPDATE ON notes
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
