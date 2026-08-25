---
name: tracking-docs
description: Use for analytics-tracking documentation work across your app portfolio - documenting a new analytics event, asking how an app tracks something, updating existing tracking doc pages, reviewing or correcting tracking conventions, or drafting a tracking implementation user story. This is a TEMPLATE - fill in references/app-registry-template.md with your own apps and docs locations before it can do anything. Do NOT use for general note-taking or docs routing that has no analytics-tracking dimension, or for analyzing the collected data itself.
---

# Tracking Docs (template)

> This skill was seeded from a real, production tracking-documentation assistant (a team
> documenting analytics events for a 9-app portfolio in Notion) and generalized into a template.
> The WORKFLOW ships complete - app resolution, the asking-vs-requesting gate, the interview, the
> propose-approve-execute protocol, the feedback loop. The REGISTRY does not: your apps, your
> docs tree, and your conventions live in `references/app-registry-template.md`, which is a
> fill-in skeleton. The skill cannot document anything until you fill it in.

Interview the user about app changes, compare against the existing tracking documentation, and
propose + write documentation with explicit approval before every write. The docs tool is
assumed to be Notion below; any docs tool with search/read/write access works the same way.

## Safety rules (non-negotiable)

1. Propose -> explicit approval -> execute, for every docs write. No exceptions, no silent writes.
2. HARD STOP after a successful write - do not chain into anything else in the same reply.
3. Never delete pages or content unless explicitly asked. Add and edit only.
4. Any work-tracker access (fetching a ticket for context) is READ-ONLY.
5. Never simulate a write that did not happen, and never claim an analytics platform (GA4, GTM, a
   warehouse) was checked live when it was not - this skill documents; it does not call
   analytics APIs.
6. Never offer or invent an app outside the registry. Apps that exist but are deliberately
   untracked are listed there as NOT offerable - a docs page about an untracked app is not
   evidence that it is tracked.

## Resolve the app first

Every turn, resolve which registry app the user means against
`references/app-registry-template.md` before doing anything else. If the message names an app,
match it; if it is genuinely ambiguous, ask - but ONLY offer apps from the registry. And never
ask the user for a docs page ID: search the app's docs tree yourself and resolve the parent page
before presenting anything.

## Mode routing (decide this first, every turn)

| The user's message reads like | Mode |
|---|---|
| "How do we track X?", "What are the rules for Y?", "Which apps support Z?" | **Inquiry (ASKING)** |
| "Document this", "Add an event", "Update the page for..." | **Interview + document (REQUESTING)** |
| The user corrects a draft, states a convention, or gives explicit feedback | **Feedback** |

**ASKING**: research it - search the docs, read what comes back, check the conventions - then
synthesize a concise answer with sources named. Note any discrepancy between the written
conventions and what is actually documented, and say plainly what you could not find. Do NOT
propose a write and do NOT ask for approval; end the turn with the answer. Only move into the
write process if the user then explicitly asks to change something.

**REQUESTING**: follow the write process below.

**Feedback**: follow the feedback loop at the bottom.

## The write process

1. **Resolve the app**, then **resolve the target page** - search first, read what's already there.
2. **Ask clarifying questions - business requirements before technical ones:**
   - **Always ask WHY first**, even for a request that looks trivial: "What question or decision
     is this tracking meant to support, and what's the feature context?" Wait for the answer.
   - What exactly is being tracked, on which platform(s)? New event, or a change to an existing one?
   - What is the trigger condition, and which parameters does it need?
   - **Always ask for scenarios**: user flows, edge cases, failure paths, different entry points.
   - Ask about screenshots - they lift documentation quality and can be embedded.
   - If a work-tracker ticket is mentioned or clearly relevant, fetch it READ-ONLY for scope
     context and cite its URL in the proposal.
3. **Ground every parameter against the existing documentation (mandatory before drafting):**
   - Search the app's existing event pages for parameters that already cover what this event
     needs, and reuse them verbatim - don't create a synonym for an established name.
   - Treat a parameter as genuinely new only if nothing documented fits.
   - **If a genuinely new parameter is needed, stop and ask permission before including it**:
     list each one (name + one-line meaning + why nothing existing fits), show which existing
     parameters you ARE reusing, and wait for confirmation. Approval of the overall event is NOT
     approval for new parameters bundled inside it. Never bundle one silently.
4. **Build the complete specification**: event name per your naming convention, platform(s),
   parameters with types, trigger condition, parent page, any app-specific requirements from the
   registry.
5. **Draft the page per `references/doc-page-format-template.md`**, then show the FULL proposal
   (title, parent page, complete body) and ask a plain question: "Here's the draft - shall I
   create/update this page?" Write nothing before the explicit yes.
6. **On approval**: create or append the page. On denial: revise and re-propose, or stop.
7. **After a successful write:** confirm in ONE sentence with the page link -> **HARD STOP** ->
   then, as a separate labeled note, cite the app's analytics surfaces from the registry (see
   below) -> then offer rule-learning if the conversation surfaced a correction (feedback loop).

## The post-write surfaces reminder (citation, not action)

After confirming a write, look the app up in the registry and remind the user - by name/ID from
the registry, never via a live call - which analytics surfaces the change still needs to reach:

- An analytics property (e.g. GA4): if the write introduced a genuinely new parameter, note that
  it needs a custom dimension there - for the user to create in the console themselves.
- A tag manager container: if the write implies a new tag/trigger/variable, note that too.
- A warehouse dataset: if the change is behavior worth propagating into derived tables, name it.
- **Cite ONLY the surfaces the registry lists for that app.** If it lists none, say nothing at
  all - no empty "nothing applies" line.

## Starter conventions (edit to match your team)

These shipped with the seed skill and are common practice; keep, edit, or replace them, and move
the result into your registry's per-app notes where they differ by app:

- **Naming**: events and parameter keys in snake_case (`change_setting`, `firmware_version`).
  The name sent by code must match the documented name exactly.
- **Lifecycle over proliferation**: one event name covers a user journey by varying a `type`
  parameter (`start` / `success` / `fail` / `opt-in` / `opt-out`...), with `subtype` for context
  within a type. Do not mint a new event name per step. A `fail` always carries a descriptive
  failure reason sourced from the real error, not a placeholder.
- **One error field, not two**: pick one canonical failure parameter and never emit two synonyms
  on the same event.
- **Core context parameters**: define the small set every event carries (product/device
  identifiers, app version + build, OS version) and treat them as global - documented once, never
  re-listed per event.
- **Consent**: if you collect behavioral data, document the consent event and its user property,
  and which event categories legally require opt-in before firing.
- **Parameter values are strings**, even numeric-looking ones - and NEVER personal data. A
  user-given device nickname is PII; a serial number field is the boundary case to decide
  deliberately.
- **Setting changes**: one event per individual change with `setting_name`, `old_value`,
  `new_value` - never batch several changes into one push.

## Verification gates

| Gate | Checks | On fail |
|---|---|---|
| App resolved | Active app is in the registry, never invented | Ask, offering only registry apps |
| Grounding | Every parameter in a proposal is either reused from existing docs or explicitly flagged + approved as new | Stop and ask before drafting |
| Approval | A write happens only after an explicit yes to the shown proposal | Do not write; re-propose or stop |
| Reminder accuracy | The post-write reminder cites only surfaces the registry lists for that app | Re-check the app's row before citing |
| No live analytics calls | No analytics-platform API is ever invoked | This skill bundles none - structurally impossible, not just a rule |

## Feedback loop - corrections become rules

Two entry points: explicit feedback ("we always use X", "that's wrong, we call it Y"), and a
silent post-write scan of the conversation that led to a write.

The 3-signal scan: **(A)** the user corrected the draft - judge whether that exposed a GAP
(nothing in the conventions covered it -> propose a new rule) or an agent error (a rule existed
and wasn't followed -> not a new rule); when ambiguous, lean toward flagging a possible gap.
**(B)** the user stated an explicit convention -> strong candidate to codify. **(C)** no
meaningful feedback -> propose nothing.

To codify: classify it as a CORE rule (applies portfolio-wide -> this file's conventions
section), an APP-SPECIFIC rule (-> that app's notes in the registry), or a USER PREFERENCE
(-> the assistant's own memory, not a skill file). Show the exact proposed edit as old-text vs
new-text and get approval before writing it. When a correction contradicts an existing rule,
REPLACE the old text - never stack a second, contradictory version underneath it. Every edit
gets a dated changelog line in the file it touched.

## Bonus mode: tracking implementation user story

When asked to "draft a tracking implementation story", produce a copy-paste-ready text block (not
a docs write): TITLE ("Tracking Implementation: <Feature>"), DESCRIPTION (what the feature is,
which tracking surfaces are implemented, deliberate scoping decisions, link to the spec page),
SCOPE bullets (exact event/parameter/table names from the spec - never invented), OUT OF SCOPE
bullets with reasoning, ACCEPTANCE CRITERIA as Given/When/Then scenarios (one per event variant,
plus a "data reflects reality" scenario and negative scenarios), and REFERENCE links. Mirror the
stakeholder's explicit decisions in both Out of Scope and an acceptance criterion.
