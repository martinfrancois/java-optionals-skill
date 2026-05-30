---
name: java-optionals
description: Write, review, and refactor Java Optional code using best practices, improving readability, and preventing common Optional antipatterns such as null-style control flow and readability regressions. Use whenever writing, reviewing, or refactoring Java code that introduces, changes, or reasons about Optional; handles absent, missing, nullable, fallback, or default values where Optional may be appropriate; or touches isPresent/isEmpty, get/orElseThrow, orElse(null), optional.stream(), findFirst/findAny, checked exceptions inside Optional chains, or nullable control flow.
---

# Java Optional Skill

Use this skill before writing Java code that may introduce `Optional`, and when reviewing or
refactoring existing Optional code. Preserve behavior, exception contracts, public output, laziness,
and readability.

Open [references/optional-examples.md](references/optional-examples.md) for non-trivial edits,
review-only tasks, priority selectors, checked-exception cases, or benchmark-style examples.

## Core Workflow

1. Classify the Optional boundary before writing branches: fallback, error, side effect,
   boolean-only check, collection lookup, checked IO/prompt, or nullable API interop. Don't start
   ordinary value flow with an `isPresent()` skeleton.
2. Use the Optional API that matches the intent when it stays readable:
   - `map` for transforming a present value;
   - `flatMap` when the transform already returns Optional;
   - `filter` to keep a value only when a predicate matches;
   - `or` for an alternate Optional source;
   - `orElse` for cheap already-computed fallback values;
   - `orElseGet` for lazy, expensive, or side-effecting fallbacks;
   - `orElseThrow` when absence is truly an error at that boundary;
   - `ifPresent` or `ifPresentOrElse` for side-effect boundaries.

   ```java
   return findCart(cartId).map(this::toSummary).orElseGet(() -> createSummary(cartId));
   ```

3. Reject ordinary-control-flow workarounds:
   - `isPresent()` / `isEmpty()` followed by `get()` or `orElseThrow()`;
   - `orElse(null)` plus local null branching;
   - `optional.stream().toList()` or another fake collection around one Optional;
   - loops, labels, or sentinel flags that only avoid an Optional terminal result.

   ```java
   // avoid
   if (cart.isPresent()) return summarize(cart.get());
   return createSummary(cartId);

   // prefer
   return cart.map(this::summarize).orElseGet(() -> createSummary(cartId));
   ```

4. Preserve laziness. If fallback work creates state, performs IO, mutates data, calls external
   services, or is expensive, use `orElseGet(...)` or an explicit lazy branch.
5. For collection streams, use `findFirst()` only when order matters; otherwise use `findAny()`.
   Keep real lookups as streams. When stateful code consumes the match, extract an `Optional<T>`
   helper that centralizes exact and `option=value` matching.
6. For selectors, keep presence checks only for boolean-only validation. Once a value is needed,
   map or bind it once. For priority selectors, map the first Optional and use lazy fallback for
   later sources. If the domain object stores an Optional, wrap the chosen value inside the mapping
   lambda.
7. Handle special boundaries directly: use a plain branch for checked IO or prompts; keep
   `orElse(null)` only at real null-based API boundaries; return an explicit decision for
   review-only tasks.
8. Verify the result: same return values, exceptions, prompts, side effects, laziness, generated
   output, and branch order; scan sibling code for the same Optional smell.

## When To Open References

Open [references/optional-examples.md](references/optional-examples.md) when:

- you're unsure whether a stream source is a real collection or a single Optional workaround;
- a fallback has side effects or checked exceptions;
- priority selectors need a worked example;
- `findFirst()` versus `findAny()` is under review;
- you need examples for testing an agent or skill implementation.

Open [references/source-notes.md](references/source-notes.md) only when maintaining this skill or
checking why a rule exists.
