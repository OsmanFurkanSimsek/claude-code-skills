# PROJECT.md - clipnote

> Single source of truth. A fresh agent reading only this file can continue correctly.

## Goal and definition of done

clipnote: a tiny Windows CLI that appends the current clipboard text into one dated notes file
with a tag, in under two seconds per capture. Done when a capture round-trips (copy text, run
`clipnote <tag>`, entry appears in the notes file with date + tag) and the five main flows are
tested.

## Scope and non-goals

TBD (Phase 3 in progress - the Elon cuts land here).

## Current state and next action

Phase 3 (Elon) in progress; discovery was skipped (--skip-discovery). Steps 1-5 are answered in
conversation: requirements tagged (capture-to-file A; cloud sync B; GUI tray app B; multi-format
export B; search command C - unverified, Osman himself); Step 2 deleted cloud sync, the tray
app, and multi-format export, kept search as a maybe; Step 3 simplified to a single `notes.md`
and one `clipnote <tag>` command; Step 4: test loop is running the exe against a scratch file;
Step 5: nothing worth automating in v1. Next action: collect the one pre-mortem answer, then
fold the Elon outcome into this file and checkpoint to Phase 4 (Research).

## Decisions locked

- Track: build (Windows CLI, Python + pyperclip).
- Discovery skipped per --skip-discovery (existing idea, single user, no audience validation
  needed).

## Plan / workstreams

TBD (Phase 5)

## Open questions

- Pre-mortem answer pending (most likely failure in 6 months + cheap prevention).
- Is the `search` command (C-tagged) worth keeping in v1?

## Change log

- 2026-07-14: Phase 0 bootstrap done; track=build; Phases 1-2 skipped; Elon coaching started.

## Lessons

- (none yet)
