---
name: java-optionals
license: MIT
description: Write, review, and refactor Java Optional code using best practices, improving readability, and preventing common Optional antipatterns such as null-style control flow and readability regressions. Use whenever writing, reviewing, or refactoring Java code that introduces, changes, or reasons about Optional; handles absent, missing, nullable, fallback, or default values where Optional may be appropriate; or touches isPresent/isEmpty, get/orElseThrow, orElse(null), optional.stream(), findFirst/findAny, checked exceptions inside Optional chains, or nullable control flow.
---

# Java Optional Skill

Use this skill before writing Java code that may introduce `Optional`, and when reviewing or
refactoring existing Optional code. Preserve behavior, exception contracts, public output, laziness,
and readability.

Open [references/optional-examples.md](references/optional-examples.md) for worked examples and
[references/java-optional-api.md](references/java-optional-api.md) for Java-version compatibility.

## Core Workflow

0. Detect the Java baseline before choosing APIs. Check `pom.xml`, Maven compiler release/source/
   target, Gradle toolchains/source/target, CI, Dockerfiles, `.sdkmanrc`, `.java-version`, and
   README docs. If unclear, prefer Java 8-compatible code or state the assumption. Don't introduce
   Java 9+ Optional APIs, Java 11 `isEmpty()`, Java 16 `Stream.toList()`, or Java 21 sequenced
   collections unless build metadata shows support.
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
   - `map(x -> optionalReturningCall(x).orElse(null))` instead of `flatMap(...)`;
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
5. Collection lookup: keep real streams readable. Use `findAny()` only when all matches are
   equivalent; keep `findFirst()` for first-match contracts. Avoid fake Optional collections,
   mutable flags, and `Optional.of(arg).filter(collection::contains)`. For `Stream<Optional<T>>`,
   use `flatMap(Optional::stream)` on Java 9+.
6. Selectors: bind a selected value once. For priority selectors, map the first source and lazily
   fall back to later sources. Treat `Optional<Boolean>` as three states when absent has separate
   meaning. A presence check is fine when it only answers a predicate and the value isn't read.
7. Primitive Optionals: use `OptionalInt`, `OptionalLong`, and `OptionalDouble` directly when the
   domain or primitive stream already returns them. Don't box just to reuse generic examples.
   Prefer primitive terminals such as `ifPresent`, `orElse`, `orElseGet`, `orElseThrow`, and
   `stream`; avoid `isPresent()` plus `getAsInt()`, `getAsLong()`, or `getAsDouble()`.
8. Special boundaries: use a plain branch for checked IO and prompts; use `orElse(null)` only at a
   real null-based API boundary; use `orElseThrow` when absence is genuinely an error. For multiple
   non-IO Optionals before a checked prompt, select one Optional first (`or(...)` on Java 9+ or
   `map(Optional::of).orElseGet(...)` on Java 8), then branch only at the prompt.
9. Verify each changed branch. Run the repo's focused Java tests, such as `./mvnw test`,
   `mvn test`, `./gradlew test`, or the existing task for the touched code. If no test exists,
   trace a small present/absent/fallback case. Confirm the same return values, exceptions, prompts,
   side effects, laziness, generated output, and branch order; scan sibling code for the same
   Optional smell.

## References

- [optional-examples.md](references/optional-examples.md): use when the workflow needs a concrete
  pattern. It contains worked Java examples for non-trivial edits, side-effecting fallbacks,
  priority selectors, checked IO, `findFirst()` / `findAny()`, and primitive Optionals.
- [java-optional-api.md](references/java-optional-api.md): use when choosing APIs across Java 8
  through Java 26 or when primitive Optional or adjacent stream/collection APIs are involved.
