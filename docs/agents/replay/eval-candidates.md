# Replay-Derived Eval Candidates

These are candidates, not active evals. Do not promote one until the full-repository replay proves
the skill changes the outcome and the reduced eval preserves that same difference.

## Candidate 1: Checked Boundary Without Fake Optional Iterables

Source:

- [results.md](results.md), Scenario B and C.

Target failure:

- The agent removes `isPresent()` / `orElseThrow()` but introduces `OptionalSupport`,
  `OptionalValues`, `CheckedOptionals`, or another checked Optional helper.
- Or it turns one Optional into a list/iterable using `optional.stream().toList()`,
  `optional.stream()::iterator`, `optionalValues(...)`, `presentValues(...)`, or an equivalent
  helper.

Reduced shape:

- A config selector has an optional command-line value.
- If present, return it without prompting or doing IO.
- If absent, perform a prompt or checked parser fallback that can throw `IOException`.
- Another requested integer option should use `map(...).orElseGet(...)` because both branches are
  ordinary value flow.

Pass conditions:

- No fake one-Optional collection or iterable.
- No generic checked Optional helper.
- Checked prompt/parser branch remains narrow and readable.
- Requested integer branch uses direct Optional value flow.
- Present value avoids prompt/IO.
- Absent value preserves prompt order and exception behavior.

Status:

- Active as headline scenario `evals/11-checked-boundary-selection-cleanup`.
- Full-repo Scenario B passed in valid with-skill-v10 after Codex was allowed to read the installed
  skill. Hosted reduced run `019e7f40-b788-74b8-97c8-e03bf6aa8190` scored baseline `80/100` and
  with-context `100/100`, with the baseline losing the targeted Optional-quality criteria while
  preserving behavior.

## Candidate 2: Fake Optional Stream/List Cleanup

Source:

- [results.md](results.md), Scenario C.

Target failure:

- The agent is asked to clean up code that turned one Optional into `optional.stream().toList()`.
- Without the skill, it removes the fake list but hides checked IO behind a generic Optional helper.
- With the skill, it should use a narrow checked-boundary branch and direct Optional flow elsewhere.

Pass conditions:

- No `stream().toList()` when the stream source is one Optional.
- No `stream()::iterator` or iterable helper around one Optional.
- No checked Optional helper abstraction.
- Behavior, laziness, exception messages, and prompt timing are preserved.

Status:

- Reduced into reference scenario
  `evals-reference/47-checked-boundary-fake-optional-list-cleanup`.
- Not headline-active: hosted baseline runs scored `95/100` or higher and did not reproduce the
  full-repo failure where the agent introduced `OptionalValues`. Keep iterating only if a smaller
  fixture can reproduce that same bad helper move without extra prompt guardrails.

## Candidate 3: Internal `orElse(null)` Cleanup

Source:

- [results.md](results.md), Scenario A.

Target failure:

- The agent changes `isPresent()` / `get()` into `orElse(null)` plus local `if (value != null)`
  branching.

Reduced shape:

- Update-or-create flow in a simple store domain.
- Existing item should update.
- Missing item should create lazily.
- Create branch has a visible side effect or exact status string.

Pass conditions:

- Uses `map(...).orElseGet(...)` or equivalent direct Optional boundary.
- Does not use `orElse(null)` for internal control flow.
- Does not use presence-check plus value-read.
- Does not run create work when an existing item is present.

Status:

- Covered by reference upsert/workpad scenarios rather than the current focused headline suite,
  including `evals-reference/02-lazy-upsert` and
  `evals-reference/48-baseline-solved-workpad-feature-cleanup`. No new Scenario A reduction was
  needed from the broad replay.
