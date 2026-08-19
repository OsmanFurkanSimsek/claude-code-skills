# Research notes template (the `## Research notes` section of PROJECT.md)

Use this in Phase 4 to capture current-state research. It lives as a section INSIDE PROJECT.md - not as a separate RESEARCH.md - so a run produces exactly two docs. The point of the section is to make the plan auditable: someone reading PROJECT.md should be able to ask "why did you pick X over Y?" and find the answer here with a citation.

Today's date matters. The model's training cutoff is older than reality - the whole reason for this phase is to overwrite stale assumptions with current data. Always include the access date next to citations.

The template carries both track shapes. On the **Build** track, research is about libraries, versions, architecture, and pitfalls. On the **Deliverable** track, it is about the audience and what "good" looks like, format/presentation conventions, authoritative data sources and their freshness, domain facts and benchmarks, and known failure modes (misleading charts, unsourced claims, stale or double-counted data). Use the subsections that fit your track; drop the rest.

**This section is curated like everything else in PROJECT.md.** A finding that hardens into a decision moves to *Decisions locked* (with its citation) and is deleted here; open items go to the canonical *Open questions* section, never to a duplicate list here. At Phase 12 the section is compacted to only the findings still load-bearing for future work.

**Legacy runs:** projects whose earlier `/e2e` version created a separate `RESEARCH.md` keep that file for the life of the run (same content, `# RESEARCH.md - <name>` title, headings one level higher).

---

## Template body (embed in PROJECT.md; copy and adapt)

```markdown
## Research notes
<!-- e2e-owned section: Phase 4 findings with citations (access dates mandatory). Curated: findings
that harden into decisions move to Decisions locked and are deleted here; open items go to Open
questions. Compacted at Phase 12 to only still-load-bearing reference material. -->

### Research questions

What we needed to answer before planning:

1. <Build: e.g., "Which JS framework is current default for new SSR apps as of <date>?" Deliverable: e.g., "What deck structure do exec audiences expect for a go/no-go decision?">
2. <Build: e.g., "What database fits a write-heavy event log under 1M events/day?" Deliverable: e.g., "Which is the source-of-record dataset for churn, and how fresh is it?">
3. <...>

### Tools / methods / sources

> Build: frameworks, libraries, runtimes. Deliverable: tools (BI platform, notebook), methods
> (analysis technique, chart types), and source datasets.

| Choice | Version / freshness (as of <date>) | Why this over alternatives | Source |
|--------|------------------------------------|----------------------------|--------|
| <name> | <version or "data as of <date>"> | <one-line rationale> | <URL, accessed <date>> |

### Patterns / conventions

- **<Build: architecture pattern | Deliverable: format/presentation convention>** - <brief description and why it fits>. Source: <URL, accessed <date>>.
- **<...>** - <...>

### Data layer

> Build: storage/schema. Deliverable: the source datasets, how they're joined, and their trust level.

- **Source / storage:** <Build: SQLite / Postgres / DynamoDB / flat files. Deliverable: which export/system of record, refresh cadence, owner>
- **Schema / shape sketch:** <key tables/collections/fields and relationships>
- **Why:** <constraints from Elon "Question requirements" + research>
- **Source:** <URL, accessed <date>>

### Pitfalls and known issues

- <Build: e.g., "Library X v3 deprecated method Y in favor of Z; migration guide at URL">
- <Deliverable: e.g., "This dataset double-counts refunds before 2024; filter on status='settled'">
- <Build: security considerations. Deliverable: misleading-visual / unsourced-claim / stale-data traps to avoid>

### Existing materials observations (only for existing-project / existing-materials runs)

> Build: filled when `claude-mem:learn-codebase` ran in Phase 4. Deliverable: existing decks, prior
> reports, established templates, or data dictionaries to reuse. Skip for greenfield / blank-slate.

- **Conventions in use:** <Build: linting rules, module style. Deliverable: brand template, naming, chart style>
- **Areas the new work touches:** <files / modules / slides / sections likely to be modified>
- **Likely integration risks:** <Build: e.g., "auth middleware caches tokens 5 min". Deliverable: e.g., "the prior report used a different fiscal-year definition">
```

## Notes for the writer

- **Don't pad.** Research that's not load-bearing for the plan is noise. If a finding doesn't make it into a *Decisions locked* bullet or an Execution plan step, omit it.
- **Cite real URLs.** Vague claims like "the React docs say…" or "the data shows…" without a link are unverifiable later. Even one link per finding is enough.
- **Access dates are mandatory.** A version number - or a data figure - without a date is not actionable in three months.
- **No duplicate homes.** Research-surfaced decisions go to *Decisions locked* with the citation attached; research-surfaced unknowns go to the canonical *Open questions* section. This section never carries its own decisions or open-questions lists.
- **For greenfield / blank-slate work**, the existing-materials subsection is empty - say so. Don't invent observations.
- **For existing projects / materials**, that subsection is critical: Build - fill it with what `claude-mem:learn-codebase` surfaced; Deliverable - fill it with the prior decks/reports/templates/data dictionaries you found.
