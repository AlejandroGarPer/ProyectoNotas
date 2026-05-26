-- ============================================================
-- 03_seed.sql
-- Datos de ejemplo para desarrollo y pruebas.
-- ============================================================

INSERT INTO notes (name, content) VALUES

    ('Bienvenida',
     'Esta es la primera nota del sistema. Aquí puedes escribir cualquier cosa que quieras recordar.'),

    ('Lista de la compra',
     E'- Leche\n- Huevos\n- Pan integral\n- Queso manchego\n- Tomates cherry'),

    ('Ideas para el proyecto',
     E'1. Añadir autenticación de usuarios\n2. Implementar etiquetas para organizar notas\n3. Búsqueda por contenido\n4. Exportar notas a PDF\n5. Modo oscuro en el frontend'),

    ('Nota vacía de prueba',
     ''),

    ('Recordatorio reunión',
     'Reunión con el equipo el viernes a las 10:00h. Preparar demo del módulo de notas y revisar backlog del sprint.'),

    ('Fragmento de código útil',
     E'-- Consulta para ver notas recientes\nSELECT id, name, updated_at\nFROM notes\nWHERE updated_at >= NOW() - INTERVAL ''7 days''\nORDER BY updated_at DESC;'),

    ('Apuntes PostgreSQL',
     E'Comandos útiles:\n  \\l          → listar bases de datos\n  \\c notesdb  → conectar a notesdb\n  \\dt         → listar tablas\n  \\dv         → listar vistas\n  \\d notes    → describir tabla notes');
