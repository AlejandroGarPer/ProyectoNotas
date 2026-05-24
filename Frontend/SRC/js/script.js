const API = "http://localhost:5000";
let editing = false;
let currentNoteName = "";

async function loadNotes() {
  const res = await fetch(API + "/notes");
  const notes = await res.json();
  const ul = document.getElementById("notes");
  ul.innerHTML = "";

  notes.forEach(note => {
    const nameNoExt = note.name.replace(".txt", "");
    const li = document.createElement("li");

    li.innerHTML = `
      <div class="note-content" onclick="editNote('${nameNoExt}', \`${note.content}\`)">
        <strong>${note.name}</strong><br>
        ${note.content}
      </div>
      <button class="delete-btn" onclick="deleteNote('${nameNoExt}')">
        Borrar
      </button>
    `;

    ul.appendChild(li);
  });
}

async function createNote() {
  const nameInput = document.getElementById("name");
  const contentInput = document.getElementById("content");

  const name = nameInput.value;
  const content = contentInput.value;

  if (!name) {
    alert("El nombre es obligatorio");
    return;
  }

  if (editing) {
    await fetch(API + "/notes/" + currentNoteName, {
      method: "PUT",  
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, content })
    });
  } else {
    await fetch(API + "/notes", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, content })
    });
  }

  nameInput.value = "";
  contentInput.value = "";

  editing = false;
  currentNoteName = "";
  document.getElementById("save-btn").innerText = "Guardar nota";

  loadNotes();
}

async function deleteNote(name) {
  await fetch(API + "/notes/" + name, { method: "DELETE" });
  loadNotes();
}

function editNote(name, content) {
  document.getElementById("name").value = name;
  document.getElementById("content").value = content;

  editing = true;
  currentNoteName = name;

  document.getElementById("save-btn").innerText = "Actualizar nota";
}

loadNotes();