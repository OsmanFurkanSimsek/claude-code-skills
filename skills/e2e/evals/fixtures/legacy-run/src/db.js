// SQLite schema + migrations (step 1, done)
import Database from "better-sqlite3";

export function openDb(path = "notes.db") {
  const db = new Database(path);
  db.exec(`CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    body TEXT NOT NULL DEFAULT '',
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
  );`);
  return db;
}
