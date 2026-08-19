# Your Notion Workspace Map and Routing Guide (template)

Purpose: this document gives Claude full context of your Notion workspace so it can (a) write
new content to the correct place and (b) retrieve context from the correct place. Fill in every
`<placeholder>` below with your workspace's real pages, database IDs, and property names, then
delete this instruction line.

Companion file: the `notion-router` skill in this folder, which holds the operating procedure.
This file is the reference; the skill is the behavior.

## 1. Golden rules

1. NEVER delete anything in Notion (pages, rows, blocks) unless explicitly asked. Adding and
   editing are allowed; deletion is not.
2. Prefer append over rewrite. Avoid a full-page replace on existing pages.
3. Note here which pages (if any) contain sensitive personal data, so Claude knows never to copy
   their contents into chat output, project files, or other pages.
4. Note here which pages are shared with other people, so Claude keeps a careful, professional,
   append-only tone on those.
5. After every write, report back what was created or edited, with the Notion link.

## 2. Sidebar overview

| Page | ID | One-liner |
|---|---|---|
| `<Shortcuts / hub page>` | `<page id>` | What it's for |
| `<Inbox / Quick Capture>` | `<page id>` | Where unsorted input lands before you sort it |
| `<Areas>` | `<page id>` | The top-level list of life/work domains |
| `<Archive / knowledge root>` | `<page id>` | Where long-term reference material lives |

## 3. Databases: write targets with exact schemas

Use the database's data-source/collection id as the parent when creating rows. Property names
must match exactly.

### 3.1 `<Work Tasks>`
- DB id: `<...>`; collection id: `<...>`
- Properties: `<"Task Name" (title), "Status" select [...], "Priority" select [...], ...>`
- Defaults for new tasks: `<...>`

### 3.2 `<Daily To-Do>`
- DB id: `<...>`; collection id: `<...>`
- Properties: `<"Task" (title), "date:Remind:start", "Done" checkbox, ...>`

### 3.3 `<Projects / Mid-Term Tasks>`
- DB id: `<...>`; collection id: `<...>`
- Properties: `<"Name" (title), "Status" select [...], "date:Date:start", ...>`
- Each row is a project page; project notes get appended inside the row's page content.

### 3.4 `<Goals>`
- DB id: `<...>`; collection id: `<...>`
- Properties: `<"Name" (title), "Next Action" text, "date:Timeframe:start/end", ...>`

### 3.5 `<Reading List>`
- DB id: `<...>`; collection id: `<...>`
- Properties: `<"Title" (title), "URL", "Tag" select [read, not read], ...>`

Add or remove sections here to match your actual databases - this is only an illustrative set.

## 4. Note pages: structure and one-liners

- `<Short-Term Notes>` (`<page id>`): notes relevant for the next few months. Format = one toggle
  per note, appended at the end.
- `<Long-Term Notes>` (`<page id>`): permanent references. Child pages: `<list yours>`.
- Note here which of these pages contain sensitive material Claude should never copy elsewhere.

## 5. Legacy / unused

List anything that used to be active but shouldn't receive new content, so Claude doesn't
accidentally route there.

## 6. Retrieval guide

- `<"What's on my plate at work"> -> query <Work Tasks> for not-done items.`
- `<"My personal projects"> -> query <Projects> for not-done items.`
- `<"Today's small tasks"> -> query <Daily To-Do> for today, not done.`
- Add your own common questions and where the answer lives.

## 7. Owner context

A short paragraph of context about you (role, location, how you like Claude to behave when
writing here - e.g. "ask before assuming", languages you write in) helps Claude route and phrase
things the way you actually want.
