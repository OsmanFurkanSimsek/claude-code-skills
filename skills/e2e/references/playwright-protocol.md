# Playwright UI testing protocol

Phase 10 of the end-to-end-development skill. Run real browser-driven tests against the user-facing flows declared in PROJECT.md's Execution plan (legacy runs: PLAN.md), but only when there's actually a UI to test.

## Pre-flight: detect frontend

Look for any of the following signals from the project root. If none are present, this phase is a no-op - skip silently and advance to Phase 11.

**Strong signals (frontend almost certainly present):**
- `package.json` containing one of: `react`, `vue`, `svelte`, `next`, `nuxt`, `vite`, `astro`, `remix`, `solid`, `angular`, `@angular/core`.
- A directory named `app/`, `pages/`, `src/components/`, `src/routes/`, `frontend/`, `web/`, or `client/`.

**Weak signals (frontend possible - confirm with user):**
- One or more `*.html` files at the project root or in a `public/` / `static/` folder.
- A `tailwind.config.*` or `postcss.config.*` file.

If only weak signals exist, ask the user "Detected possible frontend signals (no clear framework). Run Playwright?" and let them decide.

If strong signals exist, ask: "Frontend detected at `<path>` (using `<framework>`). Run Playwright UI tests against the dev server?" Wait for yes/no.

## Pre-flight: confirm Playwright MCP availability

The protocol uses the `mcp__plugin_playwright_playwright__*` tool family. If those tools are not present in the available tool list, tell the user "Playwright MCP not installed - install with `npx @playwright/mcp@latest` or skip this phase." Do not attempt a workaround.

## Identify the dev server

1. Read `package.json` (or equivalent). Look for a `scripts.dev`, `scripts.start`, or `scripts.serve` entry.
2. If none found, ask the user "How do I start the dev server for this project?" and use what they say.
3. Note the expected URL (typically `http://localhost:3000`, `http://localhost:5173` for Vite, `http://localhost:4200` for Angular). If unsure, watch the server logs after launch.

## Launch the dev server

Use `Bash` with `run_in_background: true` to start the dev server. Capture the bash_id. Do not wait for the foreground.

```
Bash(command: "<dev start command, e.g. 'npm run dev'>", run_in_background: true)
```

Give the server a few seconds to bind. If it crashes immediately, surface the error and stop.

## Navigate and exercise the golden path

The "golden path" is the main user flow declared in the Execution plan's success criteria (PROJECT.md; legacy: PLAN.md). For a typical app this is the onboarding-to-core-action loop.

1. `mcp__plugin_playwright_playwright__browser_navigate` to the dev server URL.
2. **Accessibility tree check (required).** `mcp__plugin_playwright_playwright__browser_snapshot` to capture the accessibility tree. Verify the page exposes the expected landmarks for its type - at minimum a `heading`, `nav`, and `main`. If a key landmark is missing on a page that should have it, flag it as a finding and continue.
3. Walk through the main user flow:
   - Click on key elements (`browser_click`).
   - Type into inputs (`browser_type`).
   - Wait for transitions (`browser_wait_for`).
   - Take screenshots at key states (`browser_take_screenshot`).
4. After each click/input, snapshot and verify the expected result (page changed, element appeared, etc.).
5. **Console health check (required).** After every navigation and every interaction, run `browser_console_messages` and count `error` and `warning` entries. Any non-zero error count is a finding - surface it, diagnose, fix before advancing.

## Edge cases to exercise

Beyond the golden path, hit at least these five:

1. **Invalid input** - form validation, error messages, recovery flow.
2. **Navigation transition** - route change, modal open/close, back-button behaviour.
3. **Mobile viewport** - `browser_resize` to a phone-size width (e.g. 375×812); confirm layout holds and tap targets are reachable.
4. **Empty / zero-results state** - exercise a list, table, or search view with no data. Verify the empty-state copy is present, no spinner is stuck, no UI region looks broken.
5. **Error state** - simulate a network failure (kill the dev server during a request, or hit an invalid API path the app uses). Verify a user-visible error message appears, no white-screen-of-death, and the app recovers when conditions improve.

## Reporting

For each scenario tested, write a short note: scenario name, what was observed, pass/fail, console-error count, accessibility-landmark status. Save these notes inline in the conversation - do not write a separate `PLAYWRIGHT.md` unless the user asks.

If anything fails:
1. Surface the failure with the screenshot.
2. Diagnose the root cause (DOM error, JS error in console, server-side issue).
3. Fix it (Edit the relevant code).
4. Re-run the affected scenario.

Do not advance to Phase 11 (Simplification) with any open finding - neither a failed scenario, nor a red console error, nor a missing required landmark. The whole point of running this phase is to catch UI issues before Simplification touches the code.

## Cleanup

When done with the phase:
1. Close the browser via `mcp__plugin_playwright_playwright__browser_close`.
2. Stop the dev server (kill the background bash by its ID).
3. Note in the user-facing summary: "X scenarios passed, Y failed and were fixed."

## Common failure modes

- **Dev server doesn't start:** missing dependencies - run `npm install` (or equivalent), retry once, then surface to user if still broken.
- **Wrong URL:** the framework chose a different port - read the dev server's stdout via `Bash` output to find the actual URL.
- **Auth-gated app:** the golden path may require a logged-in state. Check CLAUDE.md / PROJECT.md's Execution plan for test credentials or a seed-user step. If not specified, ask the user before stubbing.
- **Flaky transition:** add a `browser_wait_for` with a more specific selector instead of a fixed sleep. Flakiness usually means timing is wrong, not that the test is bad.
- **Console errors during golden path:** never advance with red console errors logged. Diagnose (look at the message, check the stack frame, inspect the network tab via `browser_network_requests`), fix the underlying code, re-run the scenario.
- **Missing accessibility landmarks:** check the framework's layout - many SPAs render content into a generic `<div>` without semantic structure. Add `<main>`, `<nav>`, and proper heading levels rather than working around the check.
