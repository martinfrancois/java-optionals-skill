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

1. Classify the boundary first. For ordinary value flow, use an Optional terminal instead of
   `isPresent()`.
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
5. Collection lookup: keep real collections as streams and use `findAny()` unless order matters.
   Bind the match to one `Optional<T>`; avoid `Optional.of(arg).filter(collection::contains)` and
   mutable capture flags. When a real stream maps elements to `Optional<T>`, flatten it with
   `flatMap(Optional::stream)`; this is different from making one Optional into a fake collection.
6. Selectors: bind a value once if the code needs it; for priority selectors, map the first source
   and lazy-fallback to later sources. Treat `Optional<Boolean>` mode flags as three states when
   absent has its own behavior; don't collapse absent to `false` before prompt or auto-detect logic.
   Use presence checks only for boolean-only validation.
7. Primitive Optionals: apply the same intent-based rules to `OptionalInt`, `OptionalLong`, and
   `OptionalDouble`, using their terminals such as `ifPresent`, `orElse`, and `orElseThrow`.
8. Special boundaries: use a plain branch for checked IO/prompts; keep `orElse(null)` only at
   null-based API boundaries; return an explicit decision for review-only tasks.
9. Verify each changed branch. Run the repo's focused Java tests, such as `./mvnw test`,
   `mvn test`, `./gradlew test`, or the existing task for the touched code. If no test exists,
   trace a small present/absent/fallback case. Confirm the same return values, exceptions, prompts,
   side effects, laziness, generated output, and branch order; scan sibling code for the same
   Optional smell.

## References

- [optional-examples.md](references/optional-examples.md): use when the workflow needs a concrete
  pattern. It contains worked Java examples for non-trivial edits, side-effecting fallbacks,
  priority selectors, checked IO, `findFirst()` / `findAny()`, and eval-shaped cases.
- [source-notes.md](references/source-notes.md): use only when maintaining the skill. It records the
  real issue, failure modes, and rule provenance behind this guidance.
