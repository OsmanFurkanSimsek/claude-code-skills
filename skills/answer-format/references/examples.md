# Worked examples

Four shapes, each shown wrong then right. The rules in `SKILL.md` are easier to apply after reading one of these.

**Contents**
1. A work report
2. A pure question
3. A failure report
4. A chunked hand-off
5. A question in the middle of a live step list

---

## 1. A work report

The most common case: something was built, fixed, or changed.

### Wrong

> I've updated the caching layer. To test it, first run `npm run build`, then start the dev server with `npm run dev` and open localhost:3000 - you should see the dashboard load faster now. I refactored `cache.ts` to use an LRU eviction policy instead of the previous FIFO approach, which should reduce cache misses on the hot path significantly. I also bumped the TTL from 60s to 300s. Let me know if you see any issues!

Three problems. The actions are buried in the middle, so the reader has to find them. They are packed into one sentence, so it is easy to do the first and forget the rest. And "should reduce cache misses significantly" is a guess presented as a result - nothing was measured.

### Right

> ## Summary
>
> The dashboard now loads faster. I changed how the cache decides what to throw away, and how long it keeps things.
>
> Measured on my machine: the dashboard went from 1.4 seconds to 0.6 seconds on a warm cache. I have not tested it on a cold start, so the first load after a deploy may still be slow.
>
> ## Why
>
> The cache was throwing away entries in the order they arrived (FIFO), regardless of whether anything was still using them. The dashboard reads the same six queries on every render, so those six kept getting evicted by one-off queries and then re-fetched.
>
> I switched it to LRU, which throws away whatever has gone longest without being read. Those six hot queries now survive. I also raised how long an entry is kept from 60 seconds to 5 minutes, because the underlying data only changes hourly - a 60-second lifetime was throwing away good data for no reason.
>
> Trade-off: stale data can now be shown for up to 5 minutes instead of 1. For this dashboard that is fine, since the source updates hourly. It would not be fine for anything showing live values.
>
> Changed: `src/cache.ts`.
>
> ## What you should do
>
> 1. Build the project:
>    ```
>    npm run build
>    ```
> 2. Start the dev server:
>    ```
>    npm run dev
>    ```
> 3. Open http://localhost:3000 in your browser.
> 4. Load the dashboard twice and check that the second load feels faster.
> 5. Tell me whether the 5-minute staleness is acceptable, or if you want it back at 1 minute.

Note what step 5 does: it surfaces the one judgment call that is not the assistant's to make, as an explicit action rather than a buried question.

---

## 2. A pure question

There is no work for the reader here, so numbered steps would be noise.

**Question:** "Does this repo use pnpm or npm?"

### Wrong

> ## Summary
>
> I investigated the package manager used by this repository.
>
> ## Why
>
> I checked for lockfiles and found `pnpm-lock.yaml` in the root directory...
>
> ## What you should do
>
> 1. Use pnpm for all package operations.
> 2. Do not run npm install.

The three-section scaffolding is heavier than the answer. Worse, it invents two "actions" out of a fact, which trains the reader to skim past the actions section on messages where it matters.

### Right

> **pnpm.** There is a `pnpm-lock.yaml` at the root and no `package-lock.json`, and `package.json` pins `"packageManager": "pnpm@9.1.0"`.
>
> Running `npm install` would generate a competing `package-lock.json` and could resolve different versions, so stick to `pnpm install`.

Direct answer first, evidence second, and the practical consequence as a sentence rather than a numbered list.

---

## 3. A failure report

The temptation is to lead with what went well. Resist it - the reader needs the outcome first.

### Wrong

> ## Summary
>
> I've made good progress on the migration. The schema changes are complete, the new tables are created, and the backfill script is written and tested. There's one remaining issue with the foreign key constraint on the orders table that I wasn't able to resolve, so the migration currently fails at step 4 of 6.

The real news - it does not work - arrives in the last clause of a paragraph that opens with "good progress".

### Right

> ## Summary
>
> The migration does not work yet. It fails partway through, at step 4 of 6.
>
> The parts before that failure are done and tested: the schema changes, the new tables, and the backfill script. The blocker is a foreign key on the `orders` table that I could not resolve without a decision from you.
>
> ## Why
>
> Step 4 tries to add `orders.customer_id` as a foreign key pointing at `customers.id`. It fails because 1,847 rows in `orders` have a `customer_id` that does not exist in `customers` - orphaned records, mostly from 2023.
>
> There is no correct answer here that I can pick for you. The three options:
>
> - **Delete the orphans.** Cleanest result, but it destroys 1,847 order records permanently. If finance reports on historical orders, those numbers change.
> - **Create placeholder customers.** Keeps every order, but puts 1,847 fake customers in a table other things read from.
> - **Make the constraint nullable and null the orphans.** Keeps the orders and adds no fake data, but the constraint no longer guarantees what it was added to guarantee.
>
> I would pick the third: it preserves the data and is reversible, and the constraint still holds for every row written from now on. But this depends on what those 2023 orders are used for, which I do not know.
>
> ## What you should do
>
> 1. Check whether anything still reports on 2023 orders - ask finance if you are not sure.
> 2. Tell me which of the three options you want.
> 3. Nothing else - the migration is paused and has not changed any production data.

Step 3 is doing real work. Without it, the reader wonders whether the database is half-migrated.

---

## 4. A chunked hand-off

When the reader's part runs long, hand over 5 to 10 steps and stop.

### Wrong

A single numbered list of 23 steps covering installing a tool, authenticating, configuring it, running a migration, and verifying the result.

The reader abandons it around step 9. When they come back, neither of you knows which steps actually ran.

### Right

> ## What you should do
>
> This takes about 20 minutes total. Here is the first part - come back when you finish step 6 and I will give you the rest.
>
> 1. Install the CLI:
>    ```
>    winget install --id Acme.CLI --exact
>    ```
> 2. Close this terminal and open a new one, so it picks up the new program.
> 3. Log in:
>    ```
>    acme auth login
>    ```
> 4. Copy the code it shows you.
> 5. Paste the code into the browser page that opens, and click Authorize.
> 6. Come back here and tell me "logged in".

Three things make this work: the reader is told upfront how long the whole thing takes, the chunk ends with an explicit "come back and tell me", and step 2 exists because a freshly installed program is not visible to an already-open terminal - a real trip hazard, spent as its own line rather than tacked onto step 1.

---

## 5. A question in the middle of a live step list

The list is state the conversation owns. A follow-up question does not end it.

**Setup:** you handed over six steps. The reader comes back with:

> "wait, on step 3 - when it says paste the code, paste it where? the terminal or the browser?"

### Wrong

> Paste it into the browser. When you run `acme auth login` it prints a code and then opens a browser page with an input box - the code goes in that box, not back into the terminal.

The answer is correct and the list has vanished. The reader now has to scroll back up to find out what was left, which is the exact hunting this format exists to prevent. Worse, some readers will take the reply as closing the loop and assume they are finished.

### Right

> ## Summary
>
> Into the **browser**. Running `acme auth login` prints a code in the terminal and then opens a browser page with an input box - the code goes in that box. The terminal just waits until the browser side succeeds.
>
> That is a genuinely confusing bit of the flow: the terminal shows the code, so it looks like the terminal wants it back.
>
> ## What you should do
>
> 1. ~~Install the CLI~~ - done
> 2. ~~Open a new terminal~~ - done
> 3. **Run `acme auth login` and paste the code into the browser page**, then click Authorize - you are here.
> 4. Copy the workspace ID from the dashboard.
> 5. Paste the ID here.
> 6. Tell me once the first sync finishes and I will check the output.

Three things to notice.

**The numbers did not change.** Step 3 is still step 3, so "step 3" keeps meaning what the reader meant by it. Renumbering because two items are now done would silently redefine their words.

**Completed steps stay visible, struck through.** They cost one line each and remove all doubt about what has already happened.

**There is no Why section.** The question was small and the answer fit in the Summary. Sections are there when they earn their place, not as a template to fill.

### The variant worth watching for

Sometimes answering the question invalidates what comes next. Then the change is the headline, not a footnote:

> ## Summary
>
> Into the browser, not the terminal - and your question exposed a problem with what I gave you. **Step 4 will not work as written.** Pasting the code creates a personal token, and personal tokens cannot read the workspace ID from the dashboard; you need an org token for that.
>
> I have reissued the steps below, renumbered from 1 because the sequence genuinely changed.
>
> ## Why
>
> ...
>
> ## What you should do
>
> 1. ...

When the plan actually changes, renumber cleanly from 1 and say why. Stable numbers are for a list that is still valid, not for one that has been rewritten.

