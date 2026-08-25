# tracking-docs

A **template** skill for Claude Code that documents analytics-tracking events for a portfolio of
apps through an interview-then-write workflow: resolve the app, interview for the business
intent, ground every parameter against what is already documented, propose the full page, and
write only after an explicit yes.

## What problem it solves

Tracking documentation rots in a very specific way: every new event gets named slightly
differently, parameters multiply as synonyms, and six months later nobody can say which of
`error_message` and `failure_reason` is canonical. The fix is not more discipline - it is a
gatekeeper workflow. This skill makes the assistant that gatekeeper: it will not draft an event
without asking WHY it exists, will not introduce a parameter without first proving nothing
documented already covers it, will not write a page without showing the full draft and getting a
yes, and hard-stops after every write so approval never blurs into a chain of side effects.

The seed skill ran against a real 9-app portfolio documented in Notion. The transferable parts
all ship here:

- **app-registry routing** - every turn starts by resolving which app is meant, and only
  registry apps exist (deliberately untracked apps are listed as never-offerable)
- the **ASKING vs REQUESTING gate** - a question gets an answer, never an uninvited write proposal
- **parameter grounding** - reuse-first, and a genuinely new parameter needs its own individual
  approval, separate from the event's
- the **post-write surfaces reminder** - a citation ("this new parameter still needs a custom
  dimension in property X") instead of a live API call the assistant should not be making
- a **feedback loop** that turns corrections into rules, classified as core / app-specific /
  personal preference, with replace-not-append hygiene

## Why this ships as a template, not a ready skill

The workflow is generic; the registry is not. Your apps, their docs locations, their analytics
property and container IDs, and your team's conventions are the entire content of the routing
layer - shipping someone else's registry would be useless to you and would leak their internal
infrastructure. So the workflow ships complete and the registry is a fill-in skeleton.

## Layout

```
tracking-docs/
  SKILL.md                              # the workflow: modes, write process, gates, feedback loop
  README.md                             # this file
  references/
    app-registry-template.md            # FILL IN: your apps, docs roots, analytics surfaces
    doc-page-format-template.md         # the page format - adjust to your docs tool
```

## How to adapt it

1. Fork this folder into your own `~/.claude/skills/` (rename it if you like).
2. Fill in `references/app-registry-template.md`: one row per app, the docs root each app's pages
   live under, and the analytics surfaces (property / container / dataset) the post-write
   reminder should cite. List untracked apps explicitly.
3. Edit the "Starter conventions" section in `SKILL.md` to match your team's real naming and
   lifecycle rules - they are the source the grounding step checks against.
4. Skim `references/doc-page-format-template.md` and adjust the code-example shapes to your
   platforms.
5. Try it: ask to document one small, well-understood event and check the draft against an
   existing good page. The interview questions and the parameter-grounding step should feel
   strict - that strictness is the product.

## Dependencies

Needs tool access to your docs workspace (e.g. the Notion MCP connector) with search, read, and
write. Optional: read-only access to your work tracker so ticket references in a request can be
fetched for scope context.
