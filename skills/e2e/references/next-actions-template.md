# `next-actions-template.md` - the Next Actions file pair

Read this before writing a Next Actions handoff. It defines the naming rule, the content
structure, and the two templates (.md and interactive .html). The chat message still follows the
Communication format (Summary / Reasoning / Steps); the file pair is an additional durable copy
the user can open later, outside the chat.

## When a pair is written (recap; the trigger lives in SKILL.md)

A real handoff in Action mode: about 3+ steps the user must do themselves, or ANY chunk of the
chunking rule. Trivial asks (one command, one click) stay chat-only. Each chunk delivery gets a
NEW pair - never overwrite or edit an earlier pair; the folder is the history.

## Location and naming

Both files go in a `next-actions/` folder at the project root (create it if missing):

```
next-actions/YYYY-MM-DD_HH-MM-next-actions.md
next-actions/YYYY-MM-DD_HH-MM-next-actions.html
```

`YYYY-MM-DD_HH-MM` is the creation date and time (24h, local time), e.g.
`2026-07-17_15-40-next-actions.html`. The sortable prefix is how the user finds the latest file -
never omit it, never reuse a previous timestamp. Keep every old pair; do not archive or delete.

After writing both files, announce them in ONE chat line, e.g.:
"Wrote next-actions/2026-07-17_15-40-next-actions.md + .html - open the .html in your browser to
tick steps off as you go."

## Content structure (same order in both files)

1. **TLDR** - one plain paragraph: what the user needs to do and why it matters right now. No
   jargon. A reader who reads only this paragraph should still know what to do.
2. **Reasoning** - why this is the next step, which alternatives were considered, and why this
   path won. Plain words, honest trade-offs.
3. **What you need to understand** (optional) - include ONLY when a step depends on a concept the
   user may not know; explain it in plain language, as to a smart friend outside the field.
4. **Steps** - numbered, one action per step, super simple language, concrete verbs (run, open,
   click, type, look at). Where relevant, say what the user should see if it worked. Same bar as
   the chat Steps rule: "configure the connector" is a bug; spell out every click.

## The .md template

```markdown
# Next Actions - <project name>

> Created <YYYY-MM-DD HH:MM>. Newest file in `next-actions/` wins; older files are history.

## TLDR

<one plain paragraph: what to do and why it matters now>

## Reasoning

- **Why this is next:** <plain words>
- **Alternatives considered:** <option A - why not; option B - why not>
- **Why this path:** <the deciding reason>

## What you need to understand

<optional; delete the section if nothing needs explaining>

## Steps

- [ ] 1. <action>. You should see: <check>.
- [ ] 2. <action>.
- [ ] 3. <action>. You should see: <check>.
```

## The .html template

Fill every `{{...}}` slot; repeat the `<li>` block once per step (the "You should see" span is
optional per step); delete the whole "understand" `<details>` block when unused. Keep the file
fully self-contained: no external scripts, styles, fonts, or images - it must work by
double-clicking the file with no internet. Checkbox state persists in the browser's localStorage,
keyed by the file's own name, so every dated file keeps its own progress. Never use the long-dash
character anywhere in the content.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Next Actions - {{PROJECT}} - {{YYYY-MM-DD HH:MM}}</title>
<style>
  :root { --bg:#f4f6f8; --card:#ffffff; --ink:#1c2733; --muted:#5c6b7a; --accent:#2563eb;
    --accent-soft:#e3edfd; --ok:#188a42; --ok-soft:#e2f5e9; --border:#dde4ec; }
  @media (prefers-color-scheme: dark) {
    :root { --bg:#10161f; --card:#1a2330; --ink:#e6edf5; --muted:#93a4b5; --accent:#6ca4f8;
      --accent-soft:#1d3050; --ok:#4cc47a; --ok-soft:#173225; --border:#2b3a4d; } }
  * { box-sizing:border-box; }
  body { margin:0; font-family:"Segoe UI",system-ui,-apple-system,sans-serif; background:var(--bg);
    color:var(--ink); line-height:1.55; }
  .wrap { max-width:760px; margin:0 auto; padding:28px 16px 64px; }
  header { display:flex; flex-wrap:wrap; align-items:center; gap:8px 12px; }
  h1 { font-size:1.55rem; margin:0; }
  .badge { background:var(--accent-soft); color:var(--accent); border-radius:999px;
    padding:3px 13px; font-size:.85rem; font-weight:600; white-space:nowrap; }
  .project { color:var(--muted); margin:6px 0 22px; font-size:.95rem; }
  .card { background:var(--card); border:1px solid var(--border); border-radius:12px;
    padding:18px 20px; margin-bottom:14px; }
  h2 { font-size:.83rem; text-transform:uppercase; letter-spacing:.07em; color:var(--muted);
    margin:0 0 10px; }
  .tldr { border-left:4px solid var(--accent); }
  .tldr p { margin:0; font-size:1.05rem; }
  details.card { padding:0; }
  details.card summary { cursor:pointer; padding:14px 20px; font-weight:600; list-style:none;
    display:flex; justify-content:space-between; align-items:center; user-select:none; }
  details.card summary::-webkit-details-marker { display:none; }
  details.card summary::after { content:"show"; font-size:.8rem; font-weight:600;
    color:var(--accent); }
  details[open].card summary::after { content:"hide"; }
  details.card .body { padding:0 20px 16px; }
  details.card .body :first-child { margin-top:0; }
  details.card .body :last-child { margin-bottom:0; }
  .progress { display:flex; align-items:center; gap:12px; margin:2px 0 14px; }
  .track { flex:1; height:10px; background:var(--border); border-radius:999px; overflow:hidden; }
  .fill { height:100%; width:0%; background:var(--ok); border-radius:999px;
    transition:width .25s ease; }
  .count { font-size:.85rem; color:var(--muted); white-space:nowrap; }
  ol.steps { list-style:none; margin:0; padding:0; counter-reset:step; }
  ol.steps li { counter-increment:step; border-top:1px solid var(--border); }
  ol.steps li:first-child { border-top:none; }
  ol.steps label { display:flex; gap:12px; padding:12px 2px; cursor:pointer; align-items:flex-start; }
  ol.steps input { position:absolute; opacity:0; pointer-events:none; }
  .num { flex:none; width:28px; height:28px; border-radius:50%; border:2px solid var(--accent);
    color:var(--accent); font-weight:700; font-size:.85rem; display:flex; align-items:center;
    justify-content:center; margin-top:1px; }
  .num::before { content:counter(step); }
  li.checked .num { background:var(--ok); border-color:var(--ok); color:#fff; }
  li.checked .num::before { content:"\2713"; }
  li.checked .txt { color:var(--muted); text-decoration:line-through; }
  .txt { flex:1; }
  .see { display:block; color:var(--muted); font-size:.88rem; margin-top:3px;
    text-decoration:none !important; }
  li.checked .see { text-decoration:line-through; }
  .alldone { background:var(--ok-soft); color:var(--ok); border:1px solid var(--ok);
    border-radius:12px; padding:14px 20px; font-weight:600; margin-top:4px; }
  code { background:var(--accent-soft); border-radius:5px; padding:1px 6px; font-size:.92em; }
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>Next Actions</h1>
    <span class="badge">Created {{YYYY-MM-DD HH:MM}}</span>
  </header>
  <p class="project">{{PROJECT}} &middot; newest file in <code>next-actions/</code> wins; older files are history.</p>

  <div class="card tldr">
    <h2>TLDR - what you need to do</h2>
    <p>{{ONE PLAIN PARAGRAPH}}</p>
  </div>

  <details class="card">
    <summary>Reasoning - why this, and what else was considered</summary>
    <div class="body">
      <p><b>Why this is next:</b> {{PLAIN WORDS}}</p>
      <p><b>Alternatives considered:</b> {{OPTION A - WHY NOT; OPTION B - WHY NOT}}</p>
      <p><b>Why this path:</b> {{THE DECIDING REASON}}</p>
    </div>
  </details>

  <details class="card">
    <summary>What you need to understand</summary>
    <div class="body">
      <p>{{PLAIN-LANGUAGE EXPLANATION; DELETE THIS WHOLE DETAILS BLOCK IF UNUSED}}</p>
    </div>
  </details>

  <div class="card">
    <h2>Steps - tick each one off as you go</h2>
    <div class="progress">
      <div class="track"><div class="fill" id="fill"></div></div>
      <span class="count" id="count"></span>
    </div>
    <ol class="steps">
      <li><label><input type="checkbox"><span class="num"></span>
        <span class="txt">{{ACTION IN SUPER SIMPLE WORDS}}
          <span class="see">You should see: {{WHAT SUCCESS LOOKS LIKE}}</span>
        </span></label></li>
      <!-- repeat the <li> block above once per step -->
    </ol>
  </div>

  <div class="alldone" id="alldone" hidden>All steps done. Come back to the chat and say so, and we will continue from there.</div>
</div>
<script>
(function () {
  var key = "next-actions:" + decodeURIComponent(location.pathname.split(/[\\/]/).pop());
  var boxes = Array.prototype.slice.call(document.querySelectorAll(".steps input[type=checkbox]"));
  var saved = [];
  try { saved = JSON.parse(localStorage.getItem(key) || "[]"); } catch (e) {}
  boxes.forEach(function (b, i) {
    b.checked = !!saved[i];
    b.addEventListener("change", update);
  });
  function update() {
    try { localStorage.setItem(key, JSON.stringify(boxes.map(function (b) { return b.checked; }))); } catch (e) {}
    var done = boxes.filter(function (b) { return b.checked; }).length;
    document.getElementById("fill").style.width = (boxes.length ? (100 * done / boxes.length) : 0) + "%";
    document.getElementById("count").textContent = done + " of " + boxes.length + " done";
    document.getElementById("alldone").hidden = (done !== boxes.length || boxes.length === 0);
    boxes.forEach(function (b) { b.closest("li").classList.toggle("checked", b.checked); });
  }
  update();
})();
</script>
</body>
</html>
```

## Quality bar

- The .md and .html carry the SAME content; the .html adds interactivity, not extra information.
- Steps in the file must be at least as concrete as the chat version - the file is what the user
  opens tomorrow when the chat is gone.
- Long content still fits: the layout is single-column and readable at phone width; code snippets
  go in `<code>` (inline) and short `<pre>` blocks if truly needed.
- Do not add external links to libraries, fonts, or icons; the file must open offline.
