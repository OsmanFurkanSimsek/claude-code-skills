# Playtest checklist template (the `#### Playtest checklist` subsection of the Execution plan)

Use this when entering Phase 8 of the `/e2e` workflow **and there's a surface to walk**. The checklist lives as a subsection right below the Phase 8 detail block inside PROJECT.md's `## Execution plan` - not as a separate PLAYTEST.md. The user marks rows in the file or replies in chat; once Phase 8's Verification line is filled, the subsection is **deleted** (its outcome lives in the Verification line). Two shapes:

- **Build with a web frontend** - UI rows (cold start, golden path, edge cases, persistence, errors). The sections below are written for this shape.
- **Deliverable** (deck, report, analysis, dashboard, document) - content rows instead of UI rows: one row per major claim, section, chart, or audience flow. Keep the same Feedback column and triage rubric. See "Deliverable variant" below.

Surfaceless work (a library, a CLI with trivial output) skips the checklist and runs Phase 8 as a verbal walk-through instead.

**Legacy runs:** projects whose earlier `/e2e` version used a separate `PLAYTEST.md` keep that file for the life of the run.

The template is small on purpose. Anything longer just delays the user from actually reviewing.

---

## Template body (embed under the Phase 8 detail block; copy and adapt)

```markdown
#### Playtest checklist
<!-- Transient: deleted after Phase 8's Verification line is filled. Mark the Feedback column
`OK`, `nit: …`, `annoying: …`, or `blocker: …` - here or in chat. -->

**How to launch:** <concrete steps for getting the product running. Fill from the Execution plan /
package.json. E.g.: "dev server runs with `<dev command>` from `<absolute path>`; open <URL>". For
"fresh-start" rows: DevTools (F12) → Application → Local Storage → delete `<storage key>`, reload.
Drop what doesn't apply.>

**How to use:** <one short paragraph orienting the user on the product's core interaction model (or,
for a deliverable, how to read it). Pull from the PROJECT.md goal + decisions. Keep it scannable.>

Work top-to-bottom. Each row has a single observable outcome.

**A. Cold start & first impression**

| # | Step | Expected | Feedback |
|---|------|----------|----------|
| A1 | <load with empty state - clear localStorage if applicable, reload> | <what should appear: title, primary CTA, empty-state copy is honest, etc.> | |
| A2 | <click primary CTA> | <next state appears; affordances obvious> | |
| A3 | <hover key interactive elements> | <visual feedback (highlight, cursor, focus ring) is obvious; copy is readable> | |

**B. Golden path**

| # | Step | Expected | Feedback |
|---|------|----------|----------|
| B1 | <one row per major step in the primary user flow, in order> | <what should happen, observable on screen> | |
| B2 | <…> | <…> | |

**C. Edge cases**

| # | Step | Expected | Feedback |
|---|------|----------|----------|
| C1 | <unusual input / boundary condition / rapid action> | <handled gracefully, no console errors> | |
| C2 | <…> | <…> | |

**D. Persistence** (drop if not applicable)

| # | Step | Expected | Feedback |
|---|------|----------|----------|
| D1 | <do something that should persist, reload> | <state survives reload> | |
| D2 | <corrupt or delete the storage key, reload> | <product recovers gracefully, no crash> | |

**E. Error / boundary**

| # | Step | Expected | Feedback |
|---|------|----------|----------|
| E1 | <missing asset / network failure / offline> | <falls back gracefully, error is informative not silent> | |
| E2 | <…> | <…> | |

<Add additional groups as the project demands - audio, accessibility, multi-window, mobile viewport,
whatever the Execution plan's success criteria call out. Keep each group to ~3-6 rows; if a group
grows past that, the rows are too granular.>
```

## Deliverable variant (use these groups instead of A-E for a deck / report / dashboard / document)

```markdown
**F. First impression & framing**

| # | Step | Expected | Feedback |
|---|------|----------|----------|
| F1 | <read the title slide / executive summary> | <the ask and the "so what" are clear in 30 seconds> | |
| F2 | <skim the structure / table of contents> | <the narrative arc is obvious; sections are in a logical order> | |

**G. Claims & evidence**

| # | Step | Expected | Feedback |
|---|------|----------|----------|
| G1 | <check the headline number on <section/slide>> | <it ties to the source in the Research notes / the data export> | |
| G2 | <check each major claim has support> | <every claim is cited or backed by a chart; no unsupported assertion> | |
| G3 | <inspect the key chart> | <the visual actually supports the claim; axes honest; no misleading scale> | |

**H. Numbers reconcile**

| # | Step | Expected | Feedback |
|---|------|----------|----------|
| H1 | <cross-check a total that appears in two places> | <they match; no double-counting> | |
| H2 | <re-derive one figure from the underlying data> | <it reproduces> | |

**I. Audience fit & recommendation**

| # | Step | Expected | Feedback |
|---|------|----------|----------|
| I1 | <read as the target audience (exec / analyst / customer)> | <right altitude, right tone, no jargon they won't know> | |
| I2 | <read the recommendation / next step> | <it follows from the evidence and is actionable> | |
```

## Triage rubric (present to the user with the checklist)

- **`blocker`** - crashes, core flow broken, objectively wrong → **must fix** before Phase 9.
- **`annoying`** - works but is tedious / confusing / poorly paced → **must fix** before Phase 9.
- **`nit`** - minor polish (alignment, copy, micro-interaction, wording) → log for Phase 11 (Simplification / tighten).
- **`out-of-scope`** - violates PROJECT.md scope or v2 territory → log + reject in writing; do not fix.

**Hard rule:** Phase 9 (the critical review) does not start with any `blocker` or `annoying` row open. The deep review should only run once the user has signed off on *feel*.

---

## Notes for the writer (i.e., the calling skill at Phase 8)

- **Pick the right shape.** Build with a web frontend → groups A-E. Deliverable → groups F-I (drop A-E). Use the `track=` field in CLAUDE.md's marker to decide.
- **Source the rows from the Execution plan's success criteria + the PROJECT.md goal**, not from your own imagination. Every row should map to something the project actually promised to deliver.
- **One row = one observable outcome.** If a step has two checks, split it into two rows so the user can flag them independently.
- **Groups are not fixed.** A library with no UI doesn't need group A; a game needs an audio group; a deck needs the claims/evidence group. Add and remove groups to match the product's surface.
- **Keep the checklist short.** ~30-50 rows total is plenty. If you find yourself writing 100+ rows, the granularity is wrong - the user gets fatigued and the feedback gets noisier.
- **Do not fill the Feedback column yourself.** That column is exclusively the user's voice. Leave every cell empty when you write the checklist. The user may equally reply in chat ("B2 blocker: crash on submit") - transcribe their verdicts into the triage, not into the empty cells.
- **Cite project specifics in expected outcomes.** "Score reads zeros" is better than "menu shows empty state". The user should be able to tell at a glance whether what they're looking at matches the row's expectation.
- **Delete the subsection when Phase 8 completes.** The triage counts and fix notes go in the Phase 8 Verification line; the checklist itself is scaffolding, not durable record.
