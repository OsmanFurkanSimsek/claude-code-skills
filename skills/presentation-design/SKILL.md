---
name: presentation-design
description: Presentation-design principles that apply to EVERY presentation, deck, slide set, talk, keynote, or pitch you ask for, in any language. Use this skill whenever you're building a presentation or giving feedback on an existing one - trigger even if the word "presentation" isn't said (e.g. "prepare something I can present", "slides for my talk"). Update this skill with every new piece of feedback you get, so the same mistake never repeats.
---

# Presentation Design

*One presenter's field-tested style ("the Furkan style"): ruthlessly cut text, animate for
meaning, and QC every slide before it ships.*

All of your presentations get built to these principles. This file is a living document: every
time you give feedback, add or update the relevant principle here, then re-deliver the current
skill (see "Feedback loop" at the end for the delivery format).

## Core signature (apply to every deck, unasked)

These seven points are the signature; every other section is detail. A deck that breaks one of
them isn't finished:

1. **Minimum text.** At most 5-6 words per slide, one chunk per click. No paragraphs, no full
   sentences, no trailing periods. The slide is a cue; the presenter does the talking.
2. **Punchline language, Hormozi-level clarity.** Catchy, memorable titles; short, concrete,
   numbered, contrasting phrases ("6 = 6", "Started" / "Never finished", "Not finished?" / "Take
   it back"). In persuasion decks: give / get / guarantee structure, and the closing slide is a
   single, clear ask.
3. **Visual plus animation on every slide.** No text-only slides. As much visual weight as
   possible, clean and visually appealing motion; everything appears one click at a time (see
   "Animation standard" below for the concrete pattern library).
4. **The slide explains itself.** A visual has to say what it means without narration: label
   abstract shapes, write out what a number is counting. If the presenter can't tell what a slide
   means at a glance, the slide has failed.
5. **Every slide has a script entry**, including a "what this slide covers" line (2-3 plain
   sentences), the word-for-word spoken text, the click sequence, and likely questions. You can't
   give good feedback on a script you haven't read, so write it with the first full version - never
   defer it.
6. **One-shot delivery, don't assume - ask.** The ENTIRE deck (all slides + render QA) ships in a
   single pass, never partially. For anything ambiguous, ask numbered questions in one round, each
   with a suggested answer attached.
7. **Large type, one signature element, a consistent visual language** (detail: "Visual language"
   and "Typography").

## Deliverables (both, every presentation project)

1. **The presentation:** a single, fully offline HTML file. Opens in a browser, `F` for
   fullscreen, arrow keys / space / click to advance. No external dependencies (no CDN, no web
   fonts); an open-license font (e.g. Inter, OFL) can be embedded as base64 and the file still
   stays a single, offline file.
   - **Keyboard-shortcut trap (a real lesson, don't repeat it):** letter shortcuts (e.g. `F` for
     fullscreen) can't be checked with `e.key` alone - `e.key` depends on the input language (in
     a Cyrillic layout, the physical F key produces `а`, silently killing the shortcut). Fix:
     check the physical key code too, e.g. `e.code === 'KeyF'`, in addition to `e.key`. Arrow
     keys and space aren't affected. Add "keyboard input language EN/[other]" to the
     presentation-day checklist too.
2. **Speaker script (separate `.md` file):** slide numbers match the deck 1:1. Per slide: what's
   on screen, the click sequence, **Say** (the full, readable spoken text), **Do** (live-demo
   steps), **When you see** (what to say once a given thing appears on screen). You rehearse from
   this document. It also holds the time-budget table, prepared Q&A answers, and the current
   task list. Every slide entry opens with a "what this slide covers" line.
   - **The script is always a separate `.md` file**, sharing the deck's name and version number
     (e.g. `deck-v3.html` + `deck-v3-speech.md`), so the planned speech lines up side by side with
     the slides. No hidden notes layer goes inside the deck itself - add one only if explicitly
     asked for.

## Slide content

- One slide, one idea. At most 5-6 words or a single visual per slide; NEVER a full sentence. You
  say the sentences out loud - the slide is a memory cue, not a script.
- Short cue words or phrases, bulleted, fragmentary.
- **No trailing periods, no full sentences.** Nothing on a slide - title, phrase, line, card, even
  a backup-slide body - ends in a period or reads as a complete sentence (a footnote in muted
  gray citing a source is the one exception). Two-part emphasis lines break across a line, not a
  period ("Time" / "And backing"). Question marks are fine. Real rejections: "The bug tax." and
  "On time." - both came back for the trailing period. Sweep for periods before delivery.
- **Word choice stays positive and plain:** name the work, not the problem (e.g. "days on causes"
  got rejected in favor of "days on improvements"). A subtitle should read in one breath, not
  split across two sentences.
- **In persuasion decks, name the problem explicitly:** before the offer lands, the audience sees
  a plain-language answer to "what's the problem right now?" - don't invent a severity level;
  pull it from the source.
- The same rule applies INSIDE cards: instead of a long line, each point is a 2-4 word chunk with
  its own icon, and appears one click at a time. Long sentences inside comparison cards get
  rejected.
- Every slide needs a visual element: an icon, an SVG graphic, an illustration, a photo, a
  mockup, or a drawing. A text-only slide is not acceptable - back the text with icons and
  graphics.
- Live-demo slides get on-stage reminders: the question to ask, a "say this once the answer
  comes back" card. Never leave a demo slide bare.
- Numbers, years, dates and other facts get researched and verified online - never invented. Tell
  the presenter the source.
- No filler phrases ("there are no stupid questions" and the like) written onto a slide - say
  those out loud, don't spend slide space on them.
- Closing slide: a contact slide with your contact info, unless told otherwise.

## Logo, icon, and image rules (lessons from real mistakes - do not repeat them)

- **Brand logos are sourced as ORIGINAL vectors from the internet and embedded; a hand-drawn
  imitation logo is NOT acceptable.** Good sources: the `gilbarbara/logos` and `VectorLogoZone`
  GitHub repositories (via `raw.githubusercontent.com`). Verify brand colors at
  `brandfetch.com/{domain}`.
- **Technical trap:** a `web_fetch`-style tool will reject an `.svg` file as "not an image" - use
  `curl` via the shell to download SVGs instead.
- **Dark logo on dark background:** convert to a visible variant - prefer the brand's own
  recognized accent color (e.g. Anthropic's clay `#D97757`) over a generic swap, falling back to
  the brand's official white/light variant if there isn't one. WATCH OUT: light `fill="#000000"`
  values *inside* the SVG's paths must be replaced one by one - adding a `fill` to the SVG root
  does not override them (real failure mode: a logo stayed black on a dark background because
  only the root fill was changed).
- **SVG id collisions:** when multiple SVGs get embedded in the same HTML file, their internal
  ids (`gradient`, `defs`, etc.) must be made unique before embedding, or logos bleed each
  other's colors.
- **A file the user sends always wins:** if they send you the official logo, image, or photo
  file themselves, don't search the web for it - embed exactly what they sent (as base64).
- **Never fake a screenshot.** If one is needed and unavailable, draw a realistic mockup instead;
  swap in the real thing if and when they send it.
- **NO WATERMARKED STOCK IMAGES.** Never use or embed a watermarked preview image from
  Shutterstock, Getty, or similar - it's unlicensed, and the watermark reads on the projector. If
  the user sends you a watermarked image, don't embed it; explain why, and offer two clean
  options: (a) a freely licensed photo from a source like Pexels or Unsplash, which they download
  and send you, or (b) an illustration matching the deck's visual language. (The "their file
  always wins" rule is for licensed/clean files - it does not cover watermarked previews.)
- **Real product data rule:** in product-comparison demos (nutrition, price, specs), values are
  verified against actually-sold products from official manufacturer pages; note the access date
  and source in the script. Don't show brand names on the slide (keeps it from reading as an ad
  and keeps it neutral) - product type plus the real value is enough. If the demo asks an AI to
  tell products apart live, check the numbers actually differ by enough to make that possible,
  and note that check in your test list.
- **Character/avatar accessories are risky:** show the plain version first; only add an accessory
  (hat, glasses, etc.) if asked (real lesson: a cap tried on a character looked wrong and got
  cancelled). Skin tone, hair, and facial features should be realistic for the audience and
  geography being depicted, not a default.
- **Product/document demos:** realistic mock labels can be drawn directly into the slide (useful
  when someone will photograph the screen with a phone); after the demo, an "expected answer"
  summary strip can appear on a click.
- **Placeholders:** assets you're waiting on (a photo, video, or screenshot) get marked with a
  dashed-border, labeled placeholder box. Small assets (a photo, a logo) that do arrive get
  embedded as base64 as they come in.
- **VIDEO-EMBEDDING TRAP (a real lesson - do not repeat it):** don't embed a multi-megabyte video
  as a base64 data URI inside the HTML. Two reasons: (1) browsers generally won't play a data-URI
  video source at that size, and (2) the file size blows past a Claude project's knowledge-file
  limit, so it can't even be uploaded there. Correct approach: a clickable "watch online" link
  card on the slide, plus a local `.mp4` file on the presenting laptop's desktop; put "copy the
  mp4 locally" on the presentation-day checklist.

## Animation and transitions

- Within a slide: text, icons, and cards appear one at a time, on click (a fragment system). No
  automatic timing - pace is set by the presenter live.
- Between slides: cinematic transitions (soft fade, slide, zoom). No hard cuts.
- Photos get slow motion (Ken Burns: a slight zoom or pan). Emphasis elements get a pulse or
  glow.
- Video slides go full screen; videos are never embedded in the HTML itself (see the
  video-embedding trap above) - use a link card plus a local file.
- Respect `prefers-reduced-motion`.
- **Animation standard:** every slide's motion has to SHOW the idea, never decorate it - stay
  simple, one main move per slide, all of it click-triggered. Reusable patterns worth reaching for:
  1. A signature element that travels across the deck (a marker moving along an underline; it
     turns red/dashed through the problem section, resolves by the end).
  2. An arrow that flies in and lands DEAD CENTER on its target, with a slight shake on impact.
     Past mistake: the arrowhead was drawn off-center and never touched the middle - check where
     any directional shape (arrow, pointer, flow line) actually points in a real screenshot.
  3. A calendar/month grid that fills in on click (e.g. 6 of 20 workdays fill red, then the same
     6 boxes turn green on the next slide) - communicates "same cost, different use" in one glance.
  4. Large numbers counting up from 0 to their target.
  5. Progress bars that stop halfway (fill, stop, the remainder stays hatched) for a "started, not
     finished" idea.
  6. A symbol familiar from the audience's own world changing state on click (a company's own
     rating stars ticking from green to red was the most-praised slide in one deck) - look for a
     symbol like that for each specific audience.
  7. Self-drawing lines and grids that fade in progressively (hundreds of small icons appearing in
     a wave, some later fading or dropping) to make a large number felt rather than just read.
  8. A highlighter sweep behind a key phrase, wiping in left to right.
  9. One large shape drifting slowly in on open and close; soft scale-and-fade between slides;
     soft color transitions between light and dark backgrounds.
  10. Small repeating loops only when they carry meaning (a searching magnifying glass, a badge
      passed between team icons).
- **Render QA is mandatory, not optional.** Serve the deck locally (`python -m http.server` -
  browser automation blocks `file:` URLs); screenshot EVERY slide at its final click state, at
  both 1920x1080 and 1366x768, and actually look at each screenshot; check for overflow
  (`scrollHeight`/`scrollWidth`), a clean console, and re-run the forbidden-word and trailing-period
  sweep. Wait 2-3 seconds before the screenshot so counter animations finish. Fullscreen (`F`)
  can't be exercised in a headless browser - the presenter tries that by hand.

## Visual language

- Steve Jobs / Elon Musk simplicity: a dark, clean, cinematic background; one accent color; very
  large type.
- Design one topic-specific "signature element" (e.g. a timeline, an advancing dot) and use it
  consistently through the whole deck.
- Section headers use a letter-spaced, uppercase "eyebrow" label; system fonts only (keeps it
  offline).
- **An in-house audience gets that organization's own template**, not the dark cinematic default -
  this is a project-specific style call and never gets written back into this skill (that
  organization's colors and logo stay in that project's own design file, not here). Before
  researching a brand online, ask: "is there an existing deck or PDF already built on this
  template?" If so, measure it exactly instead of guessing - dominant colors from the page's own
  pixels, fonts via `pdffonts`, the logo re-vectorized via `pdftocairo -svg`. An hour of web
  research once produced the wrong colors and the wrong font; measuring the real template took ten
  minutes and matched exactly. If the template has no built-in warning color, ask the client which
  color to use for problem/risk content. An open-license font can still be embedded as base64; the
  "system fonts only" default is only for fonts you can't license that way.
- **Layout ideas worth borrowing from templates, in any style:** a bold title top-left; numbered
  colored squares (01, 02, 03) for agendas and ordered lists; a small tab-shaped label top-right
  for "source / scope" context (e.g. "team estimate", "whole system"); light background as the
  default, dark reserved for the 3-4 highest-impact slides (title, key equation, summary, close).
  Don't use an eyebrow label and a bold template-style title together - pick one.

## Typography and readability

- Font size scales to the audience: for an older audience or one viewing from a distance, push
  sizes noticeably larger and keep contrast high. Even small labels (captions, years) need to be
  readable from the back of the room. Default to "as large as it can be" - when in doubt, go
  bigger, and resolve any overflow with a real screen check rather than shrinking preemptively.
- **Scaling isn't text-only - it applies to every visual element.** Icons, logos, and graphics
  scale proportionally with the text, or the balance breaks (a real failure mode: only the fonts
  got enlarged on a revision pass, and the icons ended up looking too small next to the now-huge
  text).
- **Exception:** mockups representing a real device (a phone screen inside a mockup frame) stay
  realistically small.
- **If something overflows, don't shrink everything globally** - fix only the slide that
  overflows, locally (cut spacing/margins first, font size last).

## Structure and process

- Narrative arc: tell, explain, summarize. Agenda slide at the start; summary + punchline +
  contact slide at the end.
- **Speaker-intro slide:** when the audience doesn't already know the presenter (an association
  talk, a conference, an external audience), the intro slide belongs in the OPENING BLOCK - right
  after the agenda slide, before any content starts. It never gets buried mid-deck (a real
  lesson: an intro slide was moved from slide 6 to slide 3 after feedback, because burying it
  undersold the presenter before the audience had context). Content: title, company/affiliation
  logo, and a few brief trust signals (years of experience, education) as click-in rows -
  detailed background goes in the speaker script, not the slide. For an internal audience that
  already knows the presenter, the intro slide isn't required.
- Time budget as a slide-by-slide table; if the total runs over, note where to cut.
- Write reaction scripts for audience-interaction moments (e.g. "raise your hand if...") for both
  outcomes: nobody participates, or a lot of people do.
- For live demos: the prompts to read out loud are shown in large type on the slide; hide wait
  times behind other content; plan a fallback for every demo (a screen recording or a
  pre-generated output).
- **LIVE DEMOS CLUSTER TOGETHER (a real lesson):** screen-mirroring connections (QuickTime and
  similar) tend to freeze after a few idle minutes. Don't split demo slides across long
  demo-free stretches; the first demo isn't at the very opening - place it right after the
  setup/concept explanation, at the start of the demo block. Start or refresh mirroring right
  before the first demo slide, and mark any unavoidable gap over ~4 minutes in the script with
  "refresh the mirroring window if it froze."
- For sensitive topics (health, and similar), reassure the audience without alarming them; don't
  put cooling disclaimers ("this is not a diagnosis") on the slide itself - build that balance
  into the spoken script instead. Avoid claims you can't actually measure.
- Versioning: each revision is a separate file - v1, v2, v3... An old version is never edited in
  place. You work in revision cycles.
- Every new heading needed anywhere: offer at least 3 title alternatives. Until one is picked,
  the options can sit in a small parenthetical right on the slide; once decided, delete that line
  and the shortcut entirely.
- **One-shot delivery:** the full deck - all main slides, backup slides, script, and render QA -
  ships in one session with no approval gate mid-build; feedback then comes slide by slide.
  Before starting a long build, state the estimated time; log the actual time once it's done.
- **Don't assume, ask - same session:** contradictory or ambiguous feedback (e.g. "keep it" and
  "too much" about the same line) doesn't get silently interpreted. Ask numbered questions in one
  round, each with a suggestion and 2-4 concrete options. Names, spelling, dates, and which
  documents get produced are the client's call, not a guess.
- **Backup (reference) slides:** a `B`-key backup deck for technical follow-up questions, numbered
  B1, B2... Pressing `B` again returns to whichever main slide AND click state you left. Backup
  slides don't count in the main slide counter, and each one carries a small gray source footnote
  (the only place jargon is allowed unexplained). If the audience treats a backup topic as the
  real issue, promote it into the main deck.
- **Number traceability:** every number on a slide traces to a source line (a table in the project
  notes: number, source line, check). A team-estimated number gets a small "estimate" label on the
  slide. Never claim more than the source actually shows - a finding seen only in staging/config
  gets stamped "not yet validated in production."
- **Non-technical / executive audience:** keep a running banned-jargon list and sweep the deck for
  it before delivery; translate every technical concept into the audience's everyday language with
  a concrete example (e.g. "automations", "access packages", "an alert" rather than the internal
  term).

## Language

- This skill applies identically to any presentation language. Principles are language-
  independent.
- Presentation language: whatever's specified; if unspecified, ask based on the audience. The
  conversation language and the delivery language are independent choices.
- Never use the long-dash character, in any language, in any text.

## Context management (handoff)

On long, multi-session presentation projects, expect the chat context to get cleared and a new
one started at any point. Be ready for that:

- After every significant deliverable, close the reply with a brief status: current state,
  remaining steps (the presenter's vs. the agent's, listed separately).
- On request, produce: (1) a standalone handoff/project document (decision log, file inventory,
  remaining work, working principles) that's updated or created fresh, (2) a ready-to-paste
  prompt for a new chat, (3) a list of which files need to be (re-)uploaded to the project.
- Acceptance test: a new agent should be able to correctly continue the project from the handoff
  document alone, with nothing re-explained.
- Carry this instruction forward to future agents too - write it into the handoff document
  itself.

## Feedback loop

On a full-version delivery, hand back an interactive Next Actions HTML file: one row per slide
with OK / nit / annoying / blocker plus a note field, and a "copy feedback" button. Blocker and
annoying items always get fixed in the next revision; a slide the client says to leave alone
("keep that slide as is") stays untouched.

Every time you get feedback on a presentation:

0. Fold the feedback into this file in the SAME turn you receive it - don't make the client repeat
   themselves. Before adding anything, ask yourself: "is this a general principle, or specific to
   this one project?" Project-specific brand style (colors, logos) and single-project content
   calls (talk length, which topics to cover, how many slides) never belong here - only
   generalizable STYLE principles do (visual weight, animation, minimal text, punchy titles,
   delivery format). Keep this file GENERIC.
1. Update the deck and the script (bump the version number).
2. If the feedback generalizes into a reusable principle, add it to this SKILL.md - icon, logo,
   visual, and typography mistakes especially get written down explicitly as "past mistakes" so
   they don't repeat.
3. Re-deliver the updated skill in whatever packaged format your Claude client uses for one-click
   skill updates (keep the skill's name unchanged so it overwrites the existing skill rather than
   creating an accidental second one).
