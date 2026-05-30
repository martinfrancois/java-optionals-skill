---
name: java-optionals
description: Write, review, and refactor Java Optional code using best practices, improving readability, and preventing common Optional antipatterns such as null-style control flow and readability regressions. Use whenever writing, reviewing, or refactoring Java code that introduces, changes, or reasons about Optional; handles absent, missing, nullable, fallback, or default values where Optional may be appropriate; or touches isPresent/isEmpty, get/orElseThrow, orElse(null), optional.stream(), findFirst/findAny, checked exceptions inside Optional chains, or nullable control flow.
---

# Java Optionals

Use this skill before writing Java code that may introduce `Optional`, and when reviewing or
refactoring existing Optional code. Keep `Optional` as a clear present/absent boundary while
preserving behavior, exception contracts, public output, laziness, and readability.

This skill is based on observed production failures where agents avoided one Optional antipattern by
introducing another. Treat it as a practical guardrail, not a broad Java style guide.

Open [references/optional-examples.md](references/optional-examples.md) for non-trivial edits,
review-only tasks, checked-exception cases, or benchmark-style examples.

## Decision Procedure

1. Classify each Optional shape before editing:
   - single `Optional<T>`;
   - real collection stream ending in an Optional terminal operation;
   - boolean-only presence check;
   - absence-as-error boundary;
   - side-effecting or expensive fallback;
   - checked-exception or prompting fallback;
   - nullable interop with an API that genuinely requires `null`.
2. When writing new code, choose the Optional boundary before writing branches. Decide whether
   absence means fallback, error, side effect, prompt/IO, or nullable interop.
   Don't start with an `isPresent()` skeleton and clean it up later; write the boundary directly
   when the intent is ordinary fallback, transformation, or side-effect dispatch.
3. Reject ordinary-control-flow workarounds:
   - `optional.isPresent()` or `optional.isEmpty()` followed by `get()` or `orElseThrow()`;
   - `optional.orElse(null)` followed by local `value != null` branching;
   - `optional.stream().toList()` or similar just to loop over one Optional;
   - replacing a readable real collection stream with nested loops, labels, or sentinel flags only
     to avoid an Optional terminal result.
4. Use the Optional API that matches the intent when it stays readable:
   - `map` for transforming a present value;
   - `flatMap` when the transform already returns Optional;
   - `filter` to keep a value only when a predicate matches;
   - `or` for an alternate Optional source;
   - `orElse` for cheap already-computed fallback values;
   - `orElseGet` for lazy, expensive, or side-effecting fallbacks;
   - `orElseThrow` when absence is truly an error at that boundary;
   - `ifPresent` or `ifPresentOrElse` for side-effect boundaries.
5. Extract a named helper when a fluent chain becomes dense. Prefer a clear helper over a clever
   Optional expression.
6. Preserve laziness. If fallback work creates state, performs IO, mutates data, calls external
   services, or is expensive, use `orElseGet(...)` or an explicit lazy branch, not `orElse(...)`.
7. For review-only tasks, always return an explicit review decision. If no code change is needed,
   say that and give the Optional-shape rationale; don't return an empty answer.
8. For collection streams, choose `findFirst()` only when encounter order is part of the behavior.
   Use `findAny()` when any matching value is equivalent. When changing or intentionally keeping
   either method, include a short rationale unless the target output format is code-only.
   If a real collection lookup feeds more complex stateful code, keep the lookup as a small helper
   returning `Optional<T>` and consume that result directly. For option matchers, centralize exact
   matches and `option=value` matches in that helper instead of splitting matching logic across
   separate branches. If the surrounding loop needs a boolean such as "does this argument exactly
   equal the matched option?", derive it from the Optional value with `match.map(arg::equals).orElse(false)`
   or a named helper; don't use `match.filter(arg::equals).isPresent()` as a new presence gate.
9. For multiple independent Optional selectors, boolean-only validation may stay as presence checks
   when no value is read. Once a branch needs the value, map that Optional to the domain action or
   bind the value once; don't turn a selector into a list, stream, or null branch.
   For priority selectors, prefer a shape like:

   ```java
   return primary
           .map(value -> selectedFromPrimary(value))
           .orElseGet(() -> secondary
                   .map(value -> selectedFromSecondary(value))
                   .orElseGet(this::defaultSelection));
   ```

   If the selected domain object stores the chosen value as an `Optional`, wrap the mapped value
   with `Optional.of(value)` inside the mapping lambda rather than reopening the original Optional.
10. For checked-exception or prompting fallbacks, plain branching is acceptable:

   ```java
   Optional<String> configured = options.workspaceId();
   if (configured.isEmpty()) {
       return promptForWorkspace(terminal);
   }
   return configured.orElseThrow();
   ```

   Keep this exception narrow. The absent branch must genuinely perform checked IO, prompting, or
   another checked operation, and the enclosing method should honestly expose that boundary. When
   using this exception, say why plain branching is clearer than hiding checked exceptions in an
   unchecked wrapper or local helper unless the target output format is code-only.
11. For nullable interop, keep `orElse(null)` only at an actual API boundary that uses `null` for
   absence. Don't add local null branching around it. If changing that boundary would require
   altering records, DTOs, serialization, or external APIs, call that out as a separate API/design
   decision rather than bundling it into an Optional cleanup.

## What Not To Do

- Don't replace `isPresent()` plus `get()` with `orElse(null)` plus null checks.
- Don't force a single `Optional<T>` through stream/list syntax to avoid a branch.
- Don't ban `orElseThrow()`, `ifPresent()`, or `isPresent()` globally. Classify the shape first.
- Don't replace readable collection streams with loops merely because the stream returns Optional.
- Don't hide checked exceptions inside unchecked wrappers just to keep fluent Optional syntax.
- Don't add Vavr or another functional library for a few Optional call sites. Treat that as a
  repository-wide style decision requiring the target repository's design process.

## Review Checklist

Before finishing an Optional-related Java change, verify:

- you scanned touched code for sibling instances of the same pattern;
- ordinary `isPresent()` or `isEmpty()` plus immediate value reads are removed or justified as a
  narrow checked-exception boundary;
- no `orElse(null)` plus local null-control-flow workaround was introduced;
- no single Optional was converted to a collection or stream just to branch;
- real collection streams remain streams when clearer than manual loop state;
- `findFirst()` is used only where order matters, otherwise `findAny()` is used;
- non-obvious ordering, checked-exception, side-effect-boundary, and nullable-interop decisions are
  briefly explained when the output format allows prose;
- review-only no-op findings still include a short rationale;
- boolean-only Optional validation stays separate from value-reading branches;
- side-effecting or expensive fallbacks remain lazy;
- exception types/messages, public output, prompts, generated output, and branch order are
  preserved;
- any attractive rejected approach is documented in the form expected by the target repository.

## When To Open References

Open [references/optional-examples.md](references/optional-examples.md) when:

- you're unsure whether a stream source is a real collection or a single Optional workaround;
- a fallback has side effects or checked exceptions;
- `findFirst()` versus `findAny()` is under review;
- you need examples for testing an agent or skill implementation.

Open [references/source-notes.md](references/source-notes.md) only when maintaining this skill or
checking why a rule exists.
