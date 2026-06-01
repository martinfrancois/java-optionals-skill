---
name: java-optionals
license: MIT
description: Write, review, and refactor Java Optional code using best practices, improving readability, and preventing common Optional antipatterns such as null-style control flow and readability regressions. Use whenever writing, reviewing, or refactoring Java code that introduces, changes, or reasons about Optional; handles absent, missing, nullable, fallback, or default values where Optional may be appropriate; or touches isPresent/isEmpty, get/orElseThrow, orElse(null), optional.stream(), findFirst/findAny, checked exceptions inside Optional chains, or nullable control flow.
---

# Java Optional Skill

Use this skill before writing Java code that may introduce `Optional`, and when reviewing or
refactoring existing Optional code. Preserve behavior, exception contracts, public output, laziness,
and readability.

References: [hard-stops.md](references/hard-stops.md) for replacement antipatterns,
[optional-examples.md](references/optional-examples.md) for worked examples, and
[java-optional-api.md](references/java-optional-api.md) for Java-version compatibility.

## Hard Stops

Before finalizing touched Optional flow:

- No presence check plus value read for ordinary value flow; use value-binding Optional operations.
- No eager fallback computation before checking the Optional; keep non-trivial fallback work lazy.
- No fake one-Optional collection, iterable, loop, local `orElse(null)` branch, or generic helper.
- For checked IO, prompt, or parser branches, use the Step 6 shape and run the scan in
  [hard-stops.md](references/hard-stops.md).

## Core Workflow

0. Detect the Java baseline before choosing APIs. Check build/toolchain docs; if unclear, prefer
   Java 8-compatible code or state the assumption. Don't introduce Java 9+ Optional APIs, Java 11
   `isEmpty()`, Java 16 `Stream.toList()`, or Java 21 sequenced collections into older projects.
1. Classify the boundary first. For ordinary value flow, use an Optional terminal instead of
   `isPresent()`. When a nullable input starts an Optional flow, enter it directly with
   `Optional.ofNullable(...)` before chaining.
2. Use the Optional API that matches the intent: transform or chain with `map`/`flatMap`; use
   `orElseGet` or an explicit absent branch for non-trivial fallback work; use `orElseThrow` only
   when absence is truly an error. Don't precompute fallback results before checking the Optional.

   ```java
   return Optional.ofNullable(input).flatMap(this::lookup).orElseGet(this::fallback);
   ```

3. Collection lookup: keep real streams readable. Preserve `findFirst()` when order matters; use
   `findAny()` only when all matches are equivalent. Flatten `Stream<Optional<T>>` with
   `flatMap(Optional::stream)` on Java 9+.
4. Selectors: bind a selected value once and keep fallback lazy. Treat `Optional<Boolean>` as three
   states when absence differs from `false`. Predicate-only presence checks are fine when the value
   is not read afterward.
5. Primitive Optionals: keep `OptionalInt`, `OptionalLong`, and `OptionalDouble` primitive. Avoid
   boxing and avoid `isPresent()` plus `getAsInt()`/`getAsLong()`/`getAsDouble()`.
6. Special boundaries: use a plain branch only at a real checked IO, prompt, checked parser, or
   null-based API boundary. Before checked prompts, select any non-IO Optional value first. At the
   checked branch, don't leave `isEmpty()`/`orElseThrow()` as the present read; use the hard-stop
   empty-guard shape and add a short comment if the `get()` could be mistaken for ordinary flow.

   ```java
   if (value.isEmpty()) return readCheckedFallback();
   // Checked fallback is handled above; read the present value once.
   return value.get();
   ```

7. Verify each changed branch. Run focused tests or trace present/absent/fallback cases. Confirm
   return values, exceptions, prompts, side effects, laziness, output, and branch order. Run the
   marker scan from [hard-stops.md](references/hard-stops.md); fix relevant hits and re-scan.
