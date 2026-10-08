# Documentation page format

Loaded whenever drafting a docs page (create or append) - the exact shape a proposal's content
must take before it is shown for approval. The structure below is the seed skill's proven format;
adjust the details to your docs tool and keep the parts that enforce quality (real code examples,
a parameter table, one scenario per variant).

## Page title

Title Case, ~2-5 words, short connectors lowercase: "Add Client", "Analytics Consent", "Device
Connection Failed". The title is the human-readable feature name - NEVER the snake_case event
name (that lives in the body): title "Add Client" vs event `add_client`. For a sub-page of a
broader area use "Parent - Qualifier" with a spaced hyphen: "Setting Change - Search". Reuse the
exact product/feature name as it appears in sibling pages you found while searching. When
updating an existing page, keep its current title unless the user explicitly asks to rename it.

## Body structure

The page title is already the heading - never start the body with a heading that repeats it.
In order:

1. **When it fires** - the user action or trigger, in plain language.
2. **Screenshots** - if the user attached an image, describe the UI/copy it shows; if the message
   already contains a permanently hosted URL, embed it directly. A temporary link (chat, email)
   needs re-hosting before it can be embedded reliably - say so rather than embedding it as-is.
3. **Code examples with real values** - not placeholders, and matching the app's implementation
   method from the registry exactly:
   - Web (tag-manager dataLayer): `window.dataLayer.push({'event': 'change_setting', 'setting_name': 'Noise cancellation', 'old_value': 'off', 'new_value': 'on'})`
   - iOS (Swift): `Analytics.logEvent("change_setting", parameters: ["setting_name": "Noise cancellation", "old_value": "off", "new_value": "on"])`
   - Android (Kotlin): `firebaseAnalytics.logEvent("change_setting") { param("setting_name", "Noise cancellation"); param("old_value", "off"); param("new_value", "on") }`
   - Server-side (measurement-protocol JSON): `{"client_id": "...", "events": [{"name": "setup_completed", "params": {...}}]}`
4. **Parameter table** - columns: Key, Description, Type, Example. One row per parameter, using
   the exact snake_case names already documented for this app (grounded per the write process -
   never invented).
5. **Multiple scenarios** - one subsection per type/subtype combination that applies (start /
   success / fail, opt-in / opt-out...), each with its own code example matching that `type`
   value. For a multi-step flow, number each step, state its `type`, and give a code example per
   step - never collapse the flow into one generic example.

## What NOT to include

- No placeholder values in code examples ("your_value_here", "TODO").
- No analytics-property / tag-manager / warehouse IDs inline in the event page body - those live
  only in the registry and surface only via the post-write reminder, never as part of the
  documented event itself.
- No claim that a live analytics check was run - this skill never runs one. The page documents
  what the event IS, not a verification step.
- No personal data in example values - real-looking but synthetic device names and versions only.

## Changelog

- <date>: Initial version.
