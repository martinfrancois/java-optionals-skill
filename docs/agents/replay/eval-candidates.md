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

- Not active yet. Scenario B still fails in full-repo with-skill replay, so this should become a
  regression target only after the skill reliably avoids the fake iterable move.

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

- Best current candidate for reduction because the later with-skill replay avoided the known helper
  and fake stream/list patterns.

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

- Useful, but the full-repo scenario is broad. Prefer a reduced eval based on this shape rather than
  replaying the full prompt as a headline scenario.
