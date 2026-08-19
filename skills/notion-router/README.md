# notion-router

A **template** skill for Claude Code that routes incoming notes, tasks, and ideas into the
correct place in your own Notion workspace, and retrieves context from it on request.

## What problem it solves

If you use Notion as a personal knowledge base with more than a couple of databases (tasks,
projects, notes, goals, a reading list...), telling Claude "add this to Notion" is ambiguous -
which database, which properties, append or create? `notion-router` fixes that by giving Claude a
standing map of your workspace and a routing table, so it can classify input and write it to the
right place without you spelling it out every time.

## Why this ships as a template, not a ready skill

Unlike the other skills in this repo, there's no generic, ready-to-use version of this one - its
entire value is *your* workspace map: your actual page IDs, database schemas, and the categories
that make sense for how you personally use Notion. Shipping someone else's real map would be
useless to you (and would leak their personal data). So this folder ships the *pattern* -
routing table shape, safety rules, write mechanics - with every workspace-specific detail as a
placeholder.

## Layout

```
notion-router/
  SKILL.md                          # the routing procedure and safety rules (edit the table)
  README.md                         # this file
  references/
    notion-map-template.md          # fill this in with your own pages, database IDs, and schemas
```

## How to adapt it

1. Fork this folder (copy it into your own `~/.claude/skills/`, rename it if you like).
2. Open `references/notion-map-template.md` and replace every `<placeholder>` with your actual
   Notion pages, database ids, and exact property names.
3. Rewrite the routing table in `SKILL.md` to match the categories that exist in your workspace -
   add rows, remove rows, whatever fits. The table shipped here is illustrative only.
4. Try it: ask Claude to save a small note and see if it lands where you expect. Iterate on the
   table until it does.

## Dependencies

Needs the Notion MCP connector (or equivalent Notion tool access) enabled in your Claude Code
session - the skill only describes routing logic, it doesn't provide Notion access itself.
