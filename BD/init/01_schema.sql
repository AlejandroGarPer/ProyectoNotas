-- ============================================================
-- 01_schema.sql
-- Esquema principal de notesdb.
-- Se ejecuta automáticamente al crear el contenedor.
-- ============================================================

-- ── Tabla principal ──────────────────────────────────────────
CREATE TABLE IF NOT EXISTS notes (
    id         SERIAL                   PRIMARY KEY,
    name       VARCHAR(255)             NOT NULL UNIQUE,
    content    TEXT                     NOT NULL DEFAULT '',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ── Función y trigger para updated_at automático ─────────────
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
