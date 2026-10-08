# App registry - FILL THIS IN

Loaded at the start of every turn to resolve which app the user means, and by the post-write
step to decide which analytics-surfaces reminder to cite. Everything in `<angle brackets>` is a
placeholder. The surfaces column is INFORMATIONAL ONLY - this skill never calls an analytics
API; the IDs exist so the post-write reminder can cite them by name.

## The apps

| App ID | Name | Platforms | Docs root (page ID or URL) | Analytics surfaces |
|---|---|---|---|---|
| `<app_one_web>` | <App One (Web)> | Web | `<docs page id>` | <analytics property id> + <tag manager container id> + <warehouse dataset> |
| `<app_one_mobile_ios>` | <App One (iOS)> | iOS | `<docs page id>` | <analytics property id, shared with Android> |
| `<app_one_mobile_android>` | <App One (Android)> | Android | `<docs page id>` | <analytics property id, shared with iOS> |
| `<app_two>` | <App Two> | <platform> | `<docs page id>` | **None** - deliberately untracked surfaces stay blank |

Conventions for this table:

- **App ID** is the stable snake_case key the skill and your docs use; **Name** is what the user
  says. List every alias the user actually uses in the per-app notes below so resolution works.
- A **blank surfaces cell** means that surface does not apply - the post-write reminder stays
  silent on it. An app with no surfaces at all gets no reminder, not an empty one.
- If two platform variants share one analytics property (common for iOS/Android pairs), say so in
  the cell - it changes where a new custom dimension must be created.
- Add a **warehouse note** if your datasets live under one project/location, so the reminder can
  name the right dataset without you re-deriving it each time.

## One-line descriptions

- **<app_one_web>**: <what it is and who uses it - one line, enough to disambiguate>.
- **<app_one_mobile_ios>** / **<app_one_mobile_android>**: <same app, two platforms - say so>.
- **<app_two>**: <one line>.

## Per-app notes

### <app_one_web>
- Implementation method: <e.g. tag-manager dataLayer pushes / SDK logEvent calls / a
  server-side measurement protocol> - documented code examples must match this exactly.
- App-specific conventions: <e.g. which product-name parameter variant this app uses>.
- Aliases the user says: <"the portal", "the admin app", ...>.

### <app_one_mobile_ios>
- Implementation method: <e.g. Swift Analytics.logEvent>.
- Cross-platform note: after documenting an event here, ONE casual aside about the sibling
  platform's equivalent is allowed - never repeated, never turned into a task, and skipped
  silently if the sibling has nothing equivalent documented.

## Untracked apps (never offerable)

Apps that exist in your organization but are deliberately NOT tracked. They must never be
offered as an app choice, and a docs page describing what COULD be tracked in one is not
evidence that it is tracked - this list is.

- `<untracked app A>` - <why, and what the exception is if any (e.g. "except the migration of
  its users into <tracked app>, which we do measure")>
- `<untracked app B>`

## Changelog

- <date>: Initial version - registry seeded from <your source>.
