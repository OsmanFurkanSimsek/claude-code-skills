---
name: notion-router
description: Route notes, tasks, ideas, reminders, and knowledge into the correct place in YOUR Notion workspace, and retrieve context from it. Use this skill whenever you say anything like "add this to Notion", "save this", "note this down", "remind me", "new task", "new project", "I learned something", "what do I have on my plate", or share any experience or information worth archiving - even without mentioning Notion explicitly. Also use it before answering questions about your tasks, projects, or notes. This is a TEMPLATE - see references/notion-map-template.md and fork it for your own workspace before this skill is useful.
---

# Notion Router (template)

> This skill was seeded from a real personal Notion workspace router and generalized into a
> template. It will not do anything useful until you fork it and fill in
> `references/notion-map-template.md` with your own workspace's actual pages, database IDs, and
> property names. Treat the routing table below as an example shape, not a working destination
> list.

Operating procedure for writing to and reading from your Notion workspace. The full reference -
every page ID, database ID, and schema - lives in `references/notion-map-template.md` in this
skill's folder. Read it before the first write in a conversation.

Precondition: the Notion connector must be enabled in the current chat. If Notion tools aren't
available, say so instead of guessing or simulating a write.

## Core model (read first)

Claude writes to TWO archive places only: a **Knowledge Base** database and a **Memories**
database. Everything else is either owner-maintained (read only) or has a narrow, explicit rule
below. This replaces the older "short-term vs long-term notes" split: a time horizon says how
long something matters, not what kind of thing it is, so notes piled up in a few long pages that
nobody could search.

1. **Knowledge Base = compounding knowledge**, work AND personal. Knowledge that grows over time
   about a tool, process, system or topic: facts, contacts, IDs, how-tos, setups, lessons
   learned, incidents and their fixes. One topic page per tool/topic, built up over time (see
   Topic pages).
2. **Memories = episodic memory**: something happened and it should be remembered as a moment -
   visits, experiences, milestones, decisions.
3. **Deciding between them:** does it build knowledge about something (how it works, what to do
   next time)? -> Knowledge Base. Is it a one-off happening worth remembering as a moment? ->
   Memories. A work incident and its lesson -> Knowledge Base, NOT Memories. Meeting output ->
   Knowledge Base (decisions about a tool/topic) or Memories (a notable personal event); never a
   loose notes page.
4. **Work backlog = the owner's to manage.** Claude may ADD NOTES inside a backlog row's page
   (e.g. a dated callout at the top: what was done, result, next step, link to the Knowledge Base
   page). Claude NEVER changes status, priority, progress or any other property, and does not
   create new rows unless explicitly asked for a new task.
5. **Personal lessons:** a failure/lessons diary may be updated on Claude's own initiative when
   something relevant comes up in conversation. Confirm each write with the link.
6. **Owner-maintained pages are read only.** Hand-kept notes pages (short-term / long-term notes,
   a work-notes subtree) are SOURCE MATERIAL: Claude reads them to extract lessons and knowledge
   into the Knowledge Base or Memories, and never edits them in any way - not even a pointer line
   or a link back.

## Safety rules (non-negotiable)

1. NEVER delete pages, rows, or blocks unless explicitly asked. Add and edit only.
2. Prefer append (insert/update content) over full replace.
3. Never copy credentials or sensitive personal data out of a notes page and into chat output,
   project files, or other pages - only reference that it exists. Single optional exception: if
   you deliberately use the Knowledge Base as a password/second-brain lookup, allow credentials
   there only, on a row with a `Sensitive` checkbox checked - never in any other page, including
   backlog rows.
4. Any page shared with other people (a team page, a shared backlog) gets careful, professional,
   append-only treatment.
5. After every write, confirm with the Notion link.
6. If routing is ambiguous, ask one short question ("Knowledge Base or Memories?"); only if you
   say "just save it", fall back to a single Inbox/Quick Capture page.

## Write routing (example shape - replace with your own)

Classify the input, then write it to the matching destination. This table is a generic starting
point; your own `notion-map-template.md` should replace every row with your actual pages and
databases.

| Input type | Destination | Action |
|---|---|---|
| Tiny task / reminder | Daily To-Do database | New row: task title, reminder date |
| Note on an existing work backlog item | Work Tasks database, row page | Add notes inside the row page only; never change a property. New row only on explicit request |
| Personal project / living backlog | Projects database | New row, or append inside the matching existing project page |
| Compounding knowledge: lesson, incident + fix, how-to, tool/process knowledge, meeting output about a topic, fact, contact, ID (work or personal) | Knowledge Base database | ONE topic row per tool or topic: search for an existing topic row first and append inside it; create a row only if none exists. Single facts can be their own row |
| Episodic memory: visit, experience, event, milestone or decision worth remembering as a moment | Memories database | New row: name, date, type, location/companions if any; details inside the row page |
| Personal failure + lesson | Failure / Lessons diary | New row: what happened, lesson learned. Tool/work lessons stay in Knowledge Base topic pages |
| Open question worth tracking | Open Questions database | New row: question, area tag |
| Goal | Goals database | New row: name, next action, timeframe |
| Link to read later | Reading List database | New row: title, URL, read/unread tag |
| Unclear where it belongs | Ask one short question; Inbox / Quick Capture only on "just save it" | Append at the end; sort later |
| New life or work domain with no home yet | Areas page | Create a new subpage under Areas |

Rule of thumb: knowledge that compounds -> Knowledge Base; something that happened -> Memories;
a note on a work item -> inside its backlog row (no property changes); an ongoing project -> the
projects database; a single action -> a task database. Never write into owner-maintained notes
pages.

## Write mechanics

1. For database rows: fetch the database schema first if unsure, then create the row using the
   exact property names from your `notion-map-template.md`.
2. For row pages you add notes to (Knowledge Base, Memories, backlog, projects): match the page's
   existing style, never restructure existing content.
3. For ongoing projects: search existing rows/pages first; append inside a matching one instead
   of creating a duplicate.
4. Duplicate check: before creating a row, do a quick search for the same title; update or append
   to the existing one if it's already there.

## Topic pages (Knowledge Base)

Separate notes about the same tool or topic are lessons for the same thing, so they belong on one
Knowledge Base page. Applies to work and personal topics alike.

1. Search the Knowledge Base for the tool/topic name before writing. If a topic row exists,
   append inside it; never create a second row for the same tool.
2. New topic row properties (adapt to your schema): Name = tool/topic name, Domain = Work or
   Personal, Area = best fitting option, Term = Ongoing, Type = Process (Fact if it is a single
   fact), Sensitive checked only if the page holds credentials, Source = the pages the content
   came from, a reminder date for any real expiry/renewal (e.g. a certificate expiry).
3. Page layout: a status callout at the top (current state + next step), then numbered sections
   as needed: Account/plan, Configuration (table: field, value, who provides it), Setup order,
   How-to for users, Incident log (one dated toggle per incident), Lessons learned (numbered,
   plain language, each lesson says what to do next time), Contacts, Related pages.
4. Consolidating scattered pages about the same tool: copy the durable content (config values,
   steps, lessons, contacts) into the topic row and list the sources under Related pages. A
   one-line pointer back to the topic row may be added ONLY inside backlog row pages (notes are
   allowed there) - never into owner-maintained pages. Never delete source pages and never move
   backlog rows out of their database.
5. Label your own inferences as inferences inside the page (e.g. a suspected root cause the
   vendor did not confirm).
6. When consolidating, do not copy secrets found in other pages unless asked; link the source
   page instead.

## Retrieval routing

- Work workload -> query the Work Tasks database for not-done items.
- Personal projects -> query the Projects database for not-done items.
- Today's small tasks -> query Daily To-Do for today, not done.
- Work context -> Knowledge Base topic rows first (Domain = Work), then the related backlog row
  pages (a lot of work knowledge - owners, connection details, setup notes - gets written inline
  in task pages, so search the backlog by system name), then the owner-maintained work pages.
- Reference material (documents, contacts, how-tos) -> Knowledge Base first, then the
  owner-maintained notes pages (read only).
- Past visits, places, milestones, decisions -> the Memories database.
- Anything else domain-specific -> the matching Areas subpage.

## Resolved conflicts log

Keep a short dated log here of every routing conflict the owner has settled (e.g. "notes pages:
owner-maintained, Claude never writes"; "work incidents with lessons: Knowledge Base, not
Memories"). If a new routing conflict appears, ask one short question, then record the answer
both in the rules above and in this log, so the same question is never asked twice.

## Style

- Confirm every write briefly: what, where, the link. No fluff.
- Ask clarifying questions before a large or ambiguous write - prefer questions over assumptions.

## Keeping this skill in sync (two installs: Claude desktop/claude.ai AND Claude Code)

If you use this skill in both the Claude desktop app / claude.ai and the Claude Code terminal,
they do NOT share files. Every update must reach both, in the same conversation:

1. Update the content in every place it lives: this `SKILL.md`, `references/notion-map-template.md`
   (your filled-in copy), and any routing-guide page you keep inside Notion itself.
2. Claude desktop / claude.ai: package the folder as a `.skill` file with skill-creator's
   packager (keep the folder name unchanged) and present it, so the Update skill button appears.
   In-place edits to the mounted skill folder there do not persist across conversations, and a
   plain `.zip` has no button.
3. Claude Code terminal: also produce a `.zip` containing the skill folder (`SKILL.md` +
   `references/`). Claude Code loads personal skills from `~/.claude/skills/<skill-name>/SKILL.md`
   (Windows: `%USERPROFILE%\.claude\skills\`); install by replacing that folder, then check it
   with `/skills`.
4. When already running inside Claude Code, edit `~/.claude/skills/<skill-name>/` directly and
   still produce the desktop `.skill` package so the desktop copy matches.
5. Tool names differ between surfaces (claude.ai Notion connector vs a Notion MCP server in
   Claude Code); the routing rules are the same. If Notion tools are missing in Claude Code, add
   the Notion MCP server instead of simulating writes.

## Adapting this template to your own workspace

1. Fork this skill folder and rename it if you like (keep the frontmatter `name:` matching the
   folder name).
2. Replace every row in `references/notion-map-template.md` with your own pages, database IDs
   (or search-by-title if you don't want to hardcode IDs), and exact property names.
3. Rewrite the routing table above to match the categories that actually exist in your
   workspace - add or remove rows freely; the categories here are just an illustrative starting
   set. Keep the Core model: it is the part that makes routing decidable.
4. If you keep a duplicate copy of your routing rules inside Notion itself (handy for other
   tools/agents to read), note where that page lives here, and remember to update it whenever you
   change the routing rules.
