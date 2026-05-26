const API = "http://localhost:5000";
let editing = false;
let currentNoteId = null;

async function loadNotes() {
  try {
    const res = await fetch(`${API}/notes`);
    if (!res.ok) throw new Error(`Error cargando notas: ${res.status}`);
    const notes = await res.json();
    const ul = document.getElementById("notes");
    ul.innerHTML = "";

    notes.forEach(note => {
      const li = document.createElement("li");

      // ── Zona de texto (click para editar) ─────────────────
      const div = document.createElement("div");
      div.className = "note-content";
      div.innerHTML = `<strong>${note.name}</strong><br>${note.content}`;
      div.addEventListener("click", () => editNote(note.id, note.name, note.content));

      // ── Botón borrar ──────────────────────────────────────
      const btn = document.createElement("button");
      btn.className = "delete-btn";
      btn.textContent = "Borrar";
      btn.addEventListener("click", (e) => {
        e.stopPropagation(); // ← evita que el click suba al div y dispare editNote
        deleteNote(note.id);
      });

      li.appendChild(div);
      li.appendChild(btn);
      ul.appendChild(li);
    });
  } catch (err) {
    console.error("loadNotes:", err);
  }
}

async function createNote() {
  const nameInput    = document.getElementById("name");
  const contentInput = document.getElementById("content");
  const name         = nameInput.value.trim();
  const content      = contentInput.value;

  if (!name) {
    alert("El nombre es obligatorio");
    return;
  }

  try {
    let res;
    if (editing) {
      res = await fetch(`${API}/notes/${currentNoteId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, content })
      });
    } else {
      res = await fetch(`${API}/notes`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, content })
      });
    }

    if (!res.ok) {
      const data = await res.json();
      alert(`Error: ${data.error || res.status}`);
      return;
    }
  } catch (err) {
    alert(`Error de conexión: ${err.message}`);
    return;
  }

  // Resetear formulario
  nameInput.value    = "";
  contentInput.value = "";
  editing            = false;
  currentNoteId      = null;
  document.getElementById("save-btn").innerText = "Guardar nota";

  loadNotes();
}

async function deleteNote(id) {
  try {
    const res = await fetch(`${API}/notes/${id}`, { method: "DELETE" });
    if (!res.ok) {
      const data = await res.json();
      alert(`Error al borrar: ${data.error || res.status}`);
      return;
    }
  } catch (err) {
    alert(`Error de conexión: ${err.message}`);
    return;
  }
  loadNotes();
}

function editNote(id, name, content) {
  document.getElementById("name").value    = name;
  document.getElementById("content").value = content;

  editing       = true;
  currentNoteId = id;

  document.getElementById("save-btn").innerText = "Actualizar nota";
}

// Carga inicial
loadNotes();
