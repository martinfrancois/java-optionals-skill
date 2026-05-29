---
name: java-optionals
description: Write, review, and refactor Java Optional code using best practices, improving readability, and preventing common Optional antipatterns such as null-style control flow and readability regressions. Use whenever writing, reviewing, or refactoring Java code that introduces, changes, or reasons about Optional, isPresent/isEmpty, get/orElseThrow, orElse(null), optional.stream(), findFirst/findAny, checked exceptions inside Optional chains, or nullable control flow.
---

# Java Optionals

Use this skill before writing Optional-related Java code and when reviewing or refactoring existing
Optional code. Keep `Optional` as a clear present/absent boundary while preserving behavior,
exception contracts, public output, laziness, and readability.

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
3. Honor the requested output shape. If the task asks for a rationale, caveat, or review comment,
   include it as prose even when you also provide a code diff or replacement snippet.
4. Reject ordinary-control-flow workarounds:
   - `optional.isPresent()` or `optional.isEmpty()` followed by `get()` or `orElseThrow()`;
   - `optional.orElse(null)` followed by local `value != null` branching;
   - `optional.stream().toList()` or similar just to loop over one Optional;
   - replacing a readable real collection stream with nested loops, labels, or sentinel flags only
     to avoid an Optional terminal result.
5. Use the Optional API that matches the intent when it stays readable:
   - `map` for transforming a present value;
   - `flatMap` when the transform already returns Optional;
   - `filter` to keep a value only when a predicate matches;
   - `or` for an alternate Optional source;
   - `orElse` for cheap already-computed fallback values;
   - `orElseGet` for lazy, expensive, or side-effecting fallbacks;
   - `orElseThrow` when absence is truly an error at that boundary;
   - `ifPresent` or `ifPresentOrElse` for side-effect boundaries.
6. Extract a named helper when a fluent chain becomes dense. Prefer a clear helper over a clever
   Optional expression.
7. Preserve laziness. If fallback work creates state, performs IO, mutates data, calls external
   services, or is expensive, use `orElseGet(...)` or an explicit lazy branch, not `orElse(...)`.
8. For review-only tasks, always return an explicit review decision. If no code change is needed,
   say that and give the Optional-shape rationale; do not return an empty answer.
9. For collection streams, choose `findFirst()` only when encounter order is part of the behavior.
   Use `findAny()` when any matching value is equivalent. When changing or intentionally keeping
   either method, include a short rationale unless the target output format is code-only.
10. For multiple independent Optional selectors, boolean-only validation may stay as presence checks
   when no value is read. Once a branch needs the value, map that Optional to the domain action or
   bind the value once; do not turn a selector into a list, stream, or null branch.
11. For checked-exception or prompting fallbacks, plain branching is acceptable:

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
12. For nullable interop, keep `orElse(null)` only at an actual API boundary that uses `null` for
   absence. Do not add local null branching around it. If changing that boundary would require
   altering records, DTOs, serialization, or external APIs, call that out as a separate API/design
   decision rather than bundling it into an Optional cleanup.

## What Not To Do

- Do not replace `isPresent()` plus `get()` with `orElse(null)` plus null checks.
- Do not force a single `Optional<T>` through stream/list syntax to avoid a branch.
- Do not ban `orElseThrow()`, `ifPresent()`, or `isPresent()` globally. Classify the shape first.
- Do not replace readable collection streams with loops merely because the stream returns Optional.
- Do not hide checked exceptions inside unchecked wrappers just to keep fluent Optional syntax.
- Do not add Vavr or another functional library for a few Optional call sites. Treat that as a
  repository-wide style decision requiring the target repository's design process.

## Review Checklist

Before finishing an Optional-related Java change, verify:

- you scanned touched code for sibling instances of the same pattern;
- any requested rationale, caveat, or review comment is present in the final response;
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

- you are unsure whether a stream source is a real collection or a single Optional workaround;
- a fallback has side effects or checked exceptions;
- `findFirst()` versus `findAny()` is under review;
- you need examples for testing an agent or skill implementation.

Open [references/source-notes.md](references/source-notes.md) only when maintaining this skill or
checking why a rule exists.
