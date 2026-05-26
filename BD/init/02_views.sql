-- ============================================================
-- 02_views.sql
-- Vistas de la base de datos notesdb.
-- ============================================================


-- ── Vista: resumen de notas ───────────────────────────────────
-- Muestra cada nota con el contenido truncado a 120 caracteres,
-- útil para listados sin cargar el texto completo.
CREATE OR REPLACE VIEW v_notes_summary AS
SELECT
    id,
    name,
    CASE
        WHEN LENGTH(content) > 120
            THEN LEFT(content, 120) || '…'
        ELSE content
    END                          AS preview,
    LENGTH(content)              AS content_length,
    created_at,
    updated_at
FROM notes
ORDER BY updated_at DESC;


-- ── Vista: notas recientes (últimos 7 días) ──────────────────
-- Filtra las notas modificadas en la última semana.
CREATE OR REPLACE VIEW v_notes_recent AS
SELECT
    id,
    name,
    content,
    created_at,
    updated_at,
    NOW() - updated_at           AS time_since_update
FROM notes
WHERE updated_at >= NOW() - INTERVAL '7 days'
ORDER BY updated_at DESC;


-- ── Vista: estadísticas globales ─────────────────────────────
-- Una sola fila con métricas agregadas de toda la tabla.
CREATE OR REPLACE VIEW v_notes_stats AS
SELECT
    COUNT(*)                                    AS total_notes,
    COUNT(*) FILTER (WHERE content = '')        AS empty_notes,
    COUNT(*) FILTER (WHERE content <> '')       AS notes_with_content,
    ROUND(AVG(LENGTH(content)))                 AS avg_content_length,
    MAX(LENGTH(content))                        AS max_content_length,
    MIN(created_at)                             AS oldest_note_at,
    MAX(created_at)                             AS newest_note_at,
    MAX(updated_at)                             AS last_modified_at
FROM notes;
