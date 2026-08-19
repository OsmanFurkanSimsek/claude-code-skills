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

## Safety rules (non-negotiable)

1. NEVER delete pages, rows, or blocks unless explicitly asked. Add and edit only.
2. Prefer append (insert/update content) over full replace.
3. Never copy credentials or sensitive personal data out of a notes page and into chat output,
   project files, or other pages - only reference that it exists.
4. Any page shared with other people (a team page, a shared backlog) gets careful, professional,
   append-only treatment.
5. After every write, confirm with the Notion link.
6. If routing is ambiguous, ask one short question; if you're unavailable or say "just save it",
   fall back to a single Inbox/Quick Capture page.

## Write routing (example shape - replace with your own)

Classify the input, then write it to the matching destination. This table is a generic starting
point; your own `notion-map-template.md` should replace every row with your actual pages and
databases.

| Input type | Destination | Action |
|---|---|---|
| Tiny task / reminder | Daily To-Do database | New row: task title, reminder date |
| Work task | Work Tasks database | New row: task name, status, priority |
| Personal project / living backlog | Projects database | New row, or append inside the matching existing project page |
| Note useful for the next few months | Short-Term Notes page | Append a toggle: short title + content |
| Note worth keeping long-term | Long-Term Notes page | Append a toggle, or into a matching child page |
| Domain knowledge / meeting output | Areas > matching subpage | Existing subpage, or create a new one |
| Open question worth tracking | Open Questions database | New row: question, area tag |
| Goal | Goals database | New row: name, next action, timeframe |
| Link to read later | Reading List database | New row: title, URL, read/unread tag |
| Unclear where it belongs | Inbox / Quick Capture page | Append at the end; sort later |
| New life or work domain with no home yet | Areas page | Create a new subpage under Areas |

Time-horizon rule of thumb: a few months or less -> short-term notes; longer -> long-term notes;
an ongoing project -> the projects database; a single action -> a task database.

## Write mechanics

1. For database rows: fetch the database schema first if unsure, then create the row using the
   exact property names from your `notion-map-template.md`.
2. For note pages: append at the end (e.g. a toggle block), matching the page's existing style.
   Don't restructure existing content.
3. For ongoing projects: search existing rows/pages first; append inside a matching one instead
   of creating a duplicate.
4. Duplicate check: before creating a row, do a quick search for the same title; update or append
   to the existing one if it's already there.

## Retrieval routing

- Work workload -> query the Work Tasks database for not-done items.
- Personal projects -> query the Projects database for not-done items.
- Today's small tasks -> query Daily To-Do for today, not done.
- Reference material -> Long-Term Notes first, then Short-Term Notes.
- Anything else domain-specific -> the matching Areas subpage.

## Style

- Confirm every write briefly: what, where, the link. No fluff.
- Ask clarifying questions before a large or ambiguous write - prefer questions over assumptions.

## Adapting this template to your own workspace

1. Fork this skill folder and rename it if you like (keep the frontmatter `name:` matching the
   folder name).
2. Replace every row in `references/notion-map-template.md` with your own pages, database IDs
   (or search-by-title if you don't want to hardcode IDs), and exact property names.
3. Rewrite the routing table above to match the categories that actually exist in your
   workspace - add or remove rows freely; the categories here are just an illustrative starting
   set.
4. If you keep a duplicate copy of your routing rules inside Notion itself (handy for other
   tools/agents to read), note where that page lives here, and remember to update it whenever you
   change the routing rules.
