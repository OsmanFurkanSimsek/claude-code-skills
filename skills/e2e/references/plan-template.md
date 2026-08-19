# Execution plan template (the `## Execution plan` section of PROJECT.md)

Use this when writing the plan in Phase 5. The Execution plan is the **execution tracker**: it carries the master phase/step status table and the per-step detail. It lives as a section INSIDE PROJECT.md - not as a separate file - so a run produces exactly two docs (PROJECT.md + CLAUDE.md). It is a living section - Phase 6 (Execute) updates the status fields as steps complete; if a step uncovers a planning mistake, edit the plan to reflect new reality (and note it in *Lessons* / *Change log*). At Phase 12 the whole section is **deleted** after its outcome is folded into *Change log* / *Current state* - a finished run's step table is dead weight.

The Execution plan tracks *where we are*. The durable content (goal, scope, decisions, change log, lessons) lives in PROJECT.md's canonical sections - don't duplicate it here. CLAUDE.md is the thin bootstrap that points at PROJECT.md and carries the resume marker.

**Legacy runs:** projects whose earlier `/e2e` version created a separate `PLAN.md` keep that file for the life of the run - same table and blocks, with `# PLAN.md - <name>` as the title and headings one level higher. Never migrate a legacy run mid-flight.

A good plan has 3-8 steps. Fewer than 3 means the work is too small for `/e2e`; more than 8 means the slices are too thin or the scope too big. On the **Build** track a step is a shippable code slice; on the **Deliverable** track a step is a section/component of the artifact (a slide cluster, an analysis section, a data-model page).

---

## Template body (embed in PROJECT.md; copy and adapt)

```markdown
## Execution plan
<!-- e2e-owned section: master phase/step status table + per-step detail. Updated at every phase
and step boundary. Deleted at Phase 12 after the outcome is folded into Change log / Current state. -->

**Target:** <one paragraph: what we're building or producing, restated from the Elon outcome.>

**Architecture / structure:** <Build: e.g., "Single-binary Go CLI with cobra for arg parsing; reads
stdin/files, writes stdout/files; no network." Deliverable: e.g., "12-slide exec deck: problem ->
evidence -> 3 options -> recommendation -> ask; data from the Q3 finance export, refreshed weekly.">

### Status (master table)

> Single source of truth for where the work is. Every phase of the `/e2e` workflow AND every step
> inside Phase 6 (Execute) lives in this one table, so a fresh-context agent (post-`/clear`) can see
> at a glance what's done and what's next. Update the relevant row at every phase boundary AND at
> every step boundary inside Phase 6. Detail blocks for each row live below the table.

| # | Name | Status | Depends on | Validation / outcome |
|---|------|--------|------------|----------------------|
| 1 | Phase 1: Office Hours | <pending\|done> | - | <"distilled into Goal/Scope/Decisions"; or "skipped - `--skip-discovery`"> |
| 2 | Phase 2: CEO Review | <pending\|done> | 1 | <"scope decisions distilled into Decisions locked / non-goals"; or "skipped - `--skip-discovery`"> |
| 3 | Phase 3: Elon algorithm | <pending\|done> | 1, 2 | <"five-step outcome folded into Scope and Decisions"> |
| 4 | Phase 4: Research | <pending\|done> | 3 | <"Research notes section written"> |
| 5 | Phase 5: Plan + scaffold | <pending\|done> | 3, 4 | <"PROJECT.md at full depth + this section + CLAUDE.md finalized"> |
| 6 | Phase 6: Execute | <pending\|in_progress\|done> | 5 | <"X of N steps done" - sub-rows below> |
| 6.1 | Step 1: <Step name> | pending | - | <Build: which tests to write; Deliverable: which acceptance checks; + manual verification> |
| 6.2 | Step 2: <Step name> | pending | 6.1 | <...> |
| 6.3 | Step 3: <Step name> | pending | 6.1 | <...> |
| 7 | Phase 7: Holistic quality pass | pending | 6 | <Build: full suite green + integrated smoke + coverage ≥ thresholds (default 80/70). Deliverable: every success criterion met + whole-artifact consistency.> |
| 8 | Phase 8: Human review & feedback | pending | 7 | User-driven; Playtest checklist (surface present) or verbal walk-through; all blocker + annoying feedback fixed and re-verified. **MANDATORY before Phase 9.** |
| 9 | Phase 9: Critical review | pending | 7, 8 | All user-approved findings applied; Phase 7 verification still passes |
| 10 | Phase 10: Playwright UI testing | pending | 9 | Golden path green; or "skipped - no web frontend" |
| 11 | Phase 11: Simplification / tighten | pending | 10 | <Build: `simplify` applied. Deliverable: tighten pass.> Phase 7 + Phase 10 still pass |
| 12 | Phase 12: Final verification | pending | 11 | All rows above `done`; CLAUDE.md marker `phase=complete`; PROJECT.md finalized; this section retired |

### Step 1: <Step name>

**Goal:** <what this step delivers, in user terms>

**Implementation / production notes:**
- <Build: key file(s) to create/modify; key function or class. Deliverable: which slides/sections/
  measures to produce; the data source and any transform.>
- <any non-obvious technique to apply>

**Validation:**
- <Build: test 1 name and what it asserts; test 2 ...>
- <Deliverable: acceptance check 1 (e.g., "slide 4 total ties to the finance export"); check 2 ...>

**Manual verification:**
- <command to run / artifact to open, expected output>
- <edge case or audience perspective to exercise>

**Definition of done:**
- All validation for this step passes (Build: tests green; Deliverable: acceptance checks pass).
- Manual verification matches expected output.
- Build: no new linter/type errors introduced.

**Status:** pending → in_progress → done

### Step 2: <Step name>

<Same structure as Step 1.>

<...repeat for each step...>

### Phase 7: Holistic quality pass

**Goal:** prove the per-step pieces work together as one integrated product/artifact, and that the
whole is trustworthy.

**Checklist (Build):**
- Run the full test suite from the project root.
- **Measure coverage** with the project's tool - vitest `--coverage`, pytest `--cov`, `go test
  -coverprofile`, `cargo llvm-cov`, etc. Identify it from the "test framework" decision in Decisions
  locked + the manifest; if ambiguous, ask the user.
- Compare to the `--coverage <lines>/<branches>` thresholds (default 80/70). If below either, surface
  the gap and ask "add tests, lower the threshold, or accept as-is?" Soft-fail: never silently advance.
- Smoke-test the integrated product: launch it, exercise the main flows from the PROJECT.md goal.

**Checklist (Deliverable):**
- Review the whole artifact against the success criteria in the PROJECT.md goal (definition of done)
  and the per-step acceptance checks.
- Check cross-section consistency: no contradictions; numbers reconcile end-to-end; terminology and
  framing consistent; narrative flows.
- Confirm every success criterion is met; for any gap, ask "fix it, drop the criterion, or accept
  as-is?" (same soft-fail).
- Full read-through / dry-run as the audience would experience it.

**Both:** if anything regresses, fix it, update this section + the canonical sections, then re-run.

**Definition of done:** Build - full suite green AND coverage gate satisfied (or accepted) AND golden-path
smoke passes. Deliverable - every success criterion met AND artifact is internally consistent AND the
read-through holds.

**Status:** pending → in_progress → done

**Verification (filled when done):** <Build: suite size, pass count, coverage L%/B%, smoke summary.
Deliverable: criteria checked, consistency findings, read-through result.>

### Phase 8: Human review & feedback

**Goal:** the user actually exercises or reads the integrated product and reports what feels broken,
annoying, or wrong before the deep critical review runs. Automated checks confirm correctness; only
a human can confirm *feel* - readability, pacing, persuasiveness, frustration points.

**Why this exists separately from Phase 7:** Phase 7 asks "does it do what the plan said?" Phase 8 asks
"is what the plan said actually any good?" The Phase 9 critical review goes deep - don't aim it at work
the user has not validated.

**Checklist:**
- **If there's a surface to walk** (web frontend, or a deck/report/dashboard/document): add a
  `#### Playtest checklist` subsection right below this block, from `references/playtest-template.md`,
  with one row per major user-facing flow / claim / section (sourced from the PROJECT.md goal + this
  section's success criteria). Tell the user where to start; they mark rows in the file or in chat.
- **If there's no walkable surface** (a library, a CLI with trivial output): describe the smoke flows
  verbally and collect feedback as free text.
- User walks every row / flow and marks each `OK`, `nit: …`, `annoying: …`, or `blocker: …`.
- Triage: `blocker` and `annoying` → must fix; `nit` → log for Phase 11; `out-of-scope` → log + reject.
- For each blocker/annoying: fix, re-run the Phase 7 routine for the track, confirm no regression,
  re-walk the affected row(s).
- When done: fill the Verification line below, then **delete the Playtest checklist subsection**
  (its outcome lives in the Verification line).

**Definition of done:** checklist (or verbal feedback log) complete; nothing in `blocker` or
`annoying` open; all fixes re-verified; Phase 7 verification still green after fixes.

**Status:** pending → in_progress → done

**Verification (filled when done):** <count of feedback items by triage bucket, one-line note per
applied fix, post-fix Phase 7 result>

### Phase 9: Critical review (deep, read-only)

**Precondition:** Phase 8 is `done`; no open blocker/annoying human feedback.

**Goal:** a deep, independent, read-only review by a Claude reviewer subagent (no external CLI).
Build - a code review. Deliverable - a critical-reasoning review (logic, evidence, unsupported claims,
analytical errors, misleading visuals, structure, clarity). User picks which findings to apply; Claude
applies them.

**Checklist:**
- Spawn a read-only reviewer subagent with the prompt structure in
  `references/critical-review-protocol.md` (Build or Deliverable variant): `superpowers:code-reviewer`
  for Build, `general-purpose` for Deliverable. Instruct it to be read-only and report findings only.
  For tool artifacts it can't open, export the substance to text first or run the pass inline in
  max-thinking mode.
- Present findings grouped by severity. Ask the user which ones to fix - do NOT auto-apply.
- Apply approved fixes one by one. Re-run the Phase 7 routine for the track after fixes land. Record
  declined findings in *Decisions locked* (one terse bullet each).

**Definition of done:** all user-approved fixes applied and Phase 7 verification green afterwards.

**Status:** pending → in_progress → done

**Verification (filled when done):** <effort/model used, total findings, count by severity, count
applied, one-line note per applied fix>

### Phase 10: Playwright UI testing (conditional)

**Goal:** if a web frontend exists, exercise it end-to-end through a real browser. (Almost always
skipped on the Deliverable track.)

**Checklist:**
- Detect web frontend: Glob for `package.json` containing React / Vue / Svelte / Next / Vite / Angular,
  or `*.html`, or known frontend folders (`src/components`, `app/`, `pages/`).
- If none detected: mark this phase `skipped - no web frontend` and advance.
- If detected: ask the user "Frontend detected at `<path>` - run Playwright UI tests?" Wait for yes/no.
- If yes: identify the dev-server start command, launch it in the background, navigate via
  `mcp__plugin_playwright_playwright__browser_navigate`, exercise the golden path from this section's
  success criteria, capture snapshots/screenshots, report findings.
- Fix any UI issues found, then re-run the affected flows.

**Definition of done:** golden-path navigation completes with no console errors AND any UI fixes
applied; OR the phase is explicitly skipped because no web frontend exists.

**Status:** pending → in_progress → done

**Verification (filled when done):** <dev-server URL exercised, golden-path snapshots, UI fixes - or
"skipped - no web frontend">

### Phase 11: Simplification / tighten

**Goal:** clean dead code / redundant content without breaking anything.

**Checklist (Build):**
- Invoke `Skill(skill: "simplify")` to review and refine recently modified code.
- Re-run the full test suite (Phase 7 routine) plus the key Playwright flows if applicable.
- If anything broke, the simplification went too far - back out the offending changes, re-run.

**Checklist (Deliverable):**
- Tighten/refine pass: cut redundancy and filler, sharpen prose, drop slides/sections that don't earn
  their place, simplify the data model or measure set, remove any claim not backed by the evidence.
- Re-run the affected acceptance checks and the Phase 7 consistency review.
- If tightening dropped something load-bearing, restore it, re-check.

**Definition of done:** simplification/tighten done AND post-pass verification still green / still
consistent AND (Build) Phase 10 golden path still passes when applicable.

**Status:** pending → in_progress → done

**Verification (filled when done):** <one-line summary of what was simplified/tightened, post-pass result>

### Phase 12: Final verification & summary

**Goal:** mark the project shipped and retire this section.

**Checklist:**
- Update CLAUDE.md resume marker to `<!-- e2e-state: phase=complete track=<T> -->` and add a "Shipped"
  section listing what got built/produced and the date.
- Fold this section's outcome into the canonical sections: shipped summary + final validation results
  → *Change log* milestone line + *Current state*; step-level lessons → *Lessons*.
- **Delete this entire `## Execution plan` section** from PROJECT.md.
- Compact `## Research notes` to only still-load-bearing findings.
- Finalize PROJECT.md with the full curation sweep; print a tight one-paragraph summary for the user.

**Definition of done:** CLAUDE.md marker reads `phase=complete`, PROJECT.md finalized with this
section removed and the outcome folded into the canonical sections.

**Status:** pending → in_progress → done
```

## Notes for the writer

- **Order matters.** Steps must be in dependency order. If step 3 needs step 1's output, step 3 lists `Depends on: 1` and never starts before step 1 is `done`.
- **Each step is shippable / demonstrable.** A step should produce something real - not just scaffolding. Build: if a step has no test strategy, it's probably scaffolding and should be folded in. Deliverable: if a step produces no reviewable section, fold it in.
- **Validation is required.** Build: "automated tests + manual verification" is a hard constraint. Deliverable: "acceptance checks + manual verification". If a step truly has nothing automatable (e.g., pure visual styling, or a purely narrative slide), say so explicitly and double down on manual verification / acceptance checks.
- **Status field convention:** `pending` → `in_progress` → `done`. Avoid invented states like "blocked" - if a step is blocked, raise it with the user and note it in *Open questions*, don't write a custom status.
- **Edit the plan freely during Phase 6.** If reality diverges from the plan, the plan is wrong - fix it, and record the change in *Change log* / *Lessons*.
- **Scaffold Phases 7-12 upfront in Phase 5.** Don't wait until Phase 7 to add the headings. The user clears context often; the Execution plan must be self-explanatory at any phase boundary.
- **Phases 1-5 are pre-plan phases.** Their rows read `done` from the moment this section is written (Phase 5 is the act of expanding PROJECT.md + finalizing CLAUDE.md). They don't get detail blocks - their content is already distilled into the canonical sections.
- **One master status table, not two.** The "Status (master table)" is the single source of truth for "where are we?". When a step or phase advances, update its row's `Status` AND the matching detail block's `Status` line below. Both must agree.
- **Durable content goes in the canonical sections, not here.** Decisions, change log, and lessons live in their own sections. The Execution plan only tracks execution status and per-step detail.
- **Phase 8 is mandatory.** Always present; never delete the row. The Playtest checklist subsection is conditional (needs a walkable surface), but the *phase* is not. Surfaceless projects still gate on the user's verbal sign-off before Phase 9.
- **Numbering is 1-12, no decimals** except the 6.x execute sub-rows. State-marker name keys (`phase=critical-review` - legacy alias `codex-review` - plus `phase=playwright`, `phase=simplify`, `phase=final`, `phase=complete`, and the virtual `office-hours` and `ceo-review`) are name-keyed, not number-keyed. Legacy projects (separate PLAN.md, possibly 10-phase numbering) keep their layout and numbering for life; only new `/e2e` runs use this embedded section and 1-12.
