// Note CRUD service (step 2, done)
export function createNote(db, title, body = "") {
  return db.prepare("INSERT INTO notes (title, body) VALUES (?, ?)").run(title, body).lastInsertRowid;
}
export function getNote(db, id) {
  return db.prepare("SELECT * FROM notes WHERE id = ?").get(id);
}
export function listNotes(db) {
  return db.prepare("SELECT * FROM notes ORDER BY updated_at DESC").all();
}
export function deleteNote(db, id) {
  return db.prepare("DELETE FROM notes WHERE id = ?").run(id).changes > 0;
}
