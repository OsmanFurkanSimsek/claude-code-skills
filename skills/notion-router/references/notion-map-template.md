# Your Notion Workspace Map and Routing Guide (template)

Purpose: this document gives Claude full context of your Notion workspace so it can (a) write
new content to the correct place and (b) retrieve context from the correct place. Fill in every
`<placeholder>` below with your workspace's real pages, database IDs, and property names, then
delete this instruction line.

Companion file: the `notion-router` skill in this folder, which holds the operating procedure.
This file is the reference; the skill is the behavior.

## 0. Core model

- Knowledge Base (3.6) = compounding knowledge, work and personal: facts, contacts, how-tos,
  tool/process setups, lessons learned, incidents and fixes, meeting outputs about a topic. One
  topic page per tool/topic.
- Memories (3.7) = episodic memory: something happened and should be remembered as a moment
  (visits, experiences, milestones, decisions).
- Work Tasks (3.1) = your work backlog, managed by you. Claude only adds notes inside row pages;
  never changes status or any property; new rows only on explicit request.
- Read only for Claude (you maintain them): `<list your hand-kept notes pages>`. These are source
  material: Claude reads them, never edits them (no pointer lines either).

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
- Defaults for new tasks (only when you explicitly ask for a new task): `<...>`
- Claude only adds notes inside a row page (dated callout at top: done, result, next step, link
  to the Knowledge Base page) and never changes a property.

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

### 3.6 `<Knowledge Base>`
- DB id: `<...>`; collection id: `<...>`
- Properties: `<"Name" (title), "Domain" select [Work, Personal], "Area" select [...], "Term"
  select [Short Term, Long Term, Ongoing], "Type" select [Fact, Contact, Process, Credential,
  Other], "Sensitive" checkbox, "Source" text, "date:Reminder:start", ...>`
- Scope: general lessons and things to remember, work and personal - discrete facts and topic
  pages (one per tool/topic; layout in SKILL.md "Topic pages"). Not prompt templates or
  ideas-to-explore.

### 3.7 `<Memories>`
- DB id: `<...>`; collection id: `<...>`
- Properties: `<"Name" (title), "date:Date:start", "Type" select [...], "Location" text,
  "Companions" text, "Notes" text, ...>`
- One row per memory; short verdict in Notes, details inside the row page. Give every row a
  specific Type rather than a catch-all "Other".

Add or remove sections here to match your actual databases - this is only an illustrative set.

## 4. Note pages: structure and one-liners

- `<Short-Term Notes>` (`<page id>`): OWNER-MAINTAINED, Claude read only. Notes relevant for the
  next few months.
- `<Long-Term Notes>` (`<page id>`): OWNER-MAINTAINED, Claude read only. Permanent references.
  Child pages: `<list yours>`.
- Note here which of these pages contain sensitive material Claude should never copy elsewhere.

## 5. Legacy / unused

List anything that used to be active but shouldn't receive new content, so Claude doesn't
accidentally route there.

## 6. Retrieval guide

- `<"What's on my plate at work"> -> query <Work Tasks> for not-done items.`
- `<"My personal projects"> -> query <Projects> for not-done items.`
- `<"Today's small tasks"> -> query <Daily To-Do> for today, not done.`
- `<Context about a work topic> -> <Knowledge Base> topic rows first, then <Work Tasks> row pages
  (search by system name), then your owner-maintained work pages.`
- `<Personal reference> -> <Knowledge Base> first, then the owner-maintained notes pages.`
- `<Past visits, milestones, decisions> -> query <Memories>.`
- Add your own common questions and where the answer lives.

## 7. Owner context

A short paragraph of context about you (role, location, how you like Claude to behave when
writing here - e.g. "ask before assuming", languages you write in) helps Claude route and phrase
things the way you actually want.
