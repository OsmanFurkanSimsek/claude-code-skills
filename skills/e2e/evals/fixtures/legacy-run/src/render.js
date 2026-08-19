// Markdown rendering (step 3, in progress)
import { marked } from "marked";

export function renderNote(note) {
  return marked.parse(note.body);
}
// TODO: snapshot tests for headings, lists, code fences (step 3 validation)
