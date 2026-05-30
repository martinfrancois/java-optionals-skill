---
name: java-optionals
description: Write, review, and refactor Java Optional code using best practices, improving readability, and preventing common Optional antipatterns such as null-style control flow and readability regressions. Use whenever writing, reviewing, or refactoring Java code that introduces, changes, or reasons about Optional; handles absent, missing, nullable, fallback, or default values where Optional may be appropriate; or touches isPresent/isEmpty, get/orElseThrow, orElse(null), optional.stream(), findFirst/findAny, checked exceptions inside Optional chains, or nullable control flow.
---

# Java Optional Skill

Use this skill before writing Java code that may introduce `Optional`, and when reviewing or
refactoring existing Optional code. Preserve behavior, exception contracts, public output, laziness,
and readability.

Open [references/optional-examples.md](references/optional-examples.md) for worked examples.

## Core Workflow

1. Classify the boundary first: fallback, error, side effect, boolean check, collection lookup,
   checked IO/prompt, or nullable API. Ordinary value flow should start with an Optional terminal,
   not `isPresent()`.
2. Use the Optional API that matches the intent: `map`, `flatMap`, `filter`, `or`, `orElse` for
   cheap values, `orElseGet` for lazy fallback work, `orElseThrow` for true absence errors, and
   `ifPresent` or `ifPresentOrElse` for side effects.

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
5. Collection lookup: real collection -> stream + `findAny()` unless order matters. Stateful
   consumer -> one `Optional<T>` helper for exact and `option=value`; avoid
   `Optional.of(arg).filter(collection::contains)` and mutable capture flags.
6. Selectors: presence checks only for boolean-only validation. Value needed -> bind once. Priority
   -> map first source, lazy-fallback to later sources, wrap chosen values inside target Optional
   fields in that lambda.
7. Special boundaries: plain branch for checked IO/prompts; `orElse(null)` only at null-based API
   boundaries; explicit decision for review-only tasks.
8. Verify the result: same return values, exceptions, prompts, side effects, laziness, generated
   output, and branch order; scan sibling code for the same Optional smell.

## References

- [optional-examples.md](references/optional-examples.md): non-trivial edits, side-effecting
  fallbacks, priority selectors, checked IO, `findFirst()` / `findAny()`, eval examples.
- [source-notes.md](references/source-notes.md): maintenance and rule provenance only.
