---
name: java-optionals
license: MIT
description: Write, review, and refactor Java Optional code so that present values are bound with map, flatMap, orElseGet, or ifPresentOrElse instead of a presence check followed by a read, fallback work stays lazy, checked IO and prompt branches stay plain, findFirst or findAny follows the order contract, and null-style control flow, orElse(null) workarounds, and fake one-Optional collections are rejected. Use whenever Java code introduces, changes, or reasons about Optional; decides whether a nullable return, a missing value, or a fallback default should become an Optional; or touches isPresent/isEmpty, get/orElseThrow, orElse(null), optional.stream(), findFirst/findAny, checked exceptions inside Optional chains, or nullable control flow.
---

# Java Optional Skill

Preserve behavior, exception contracts, public output, laziness, and readability in every change.

## Reference Bundle

| File | Purpose |
|---|---|
| [hard-stops.md](references/hard-stops.md) | Replacement antipatterns and the marker scan to run |
| [optional-examples.md](references/optional-examples.md) | Worked before/after examples |
| [java-optional-api.md](references/java-optional-api.md) | Java-version compatibility for Optional APIs |

## Hard Stops

Check last, with [hard-stops.md](references/hard-stops.md), for a presence check followed by a
value read, fallback work done before the check, and one Optional turned into a collection, a
loop, an `orElse(null)` branch, or a generic unwrapping helper.

## Core Workflow

0. Check the Java baseline before choosing APIs. Read build/toolchain docs; if unclear, use Java
   8-compatible code or state the assumption. Don't add Java 9+ Optional APIs, Java 11 `isEmpty()`,
   Java 16 `Stream.toList()`, or Java 21 sequenced collections to older projects.
1. For ordinary value flow, replace guard/read code with one Optional result. Start nullable input
   with `Optional.ofNullable(...)`; don't reopen the value with `get()`.

   ```java
   Optional<Cart> cart = carts.find(cartId);

   // avoid
   if (cart.isPresent()) return summarize(cart.get());
   return createSummary(cartId);

   // prefer
   return cart.map(this::summarize).orElseGet(() -> createSummary(cartId));
   ```

   The same rule covers a presence check that only picks one of two constants:
   `promoCode.isPresent() ? Shipping.EXPRESS : Shipping.STANDARD` becomes
   `promoCode.map(code -> Shipping.EXPRESS).orElse(Shipping.STANDARD)`. When the present branch also does something (logs, sends, writes), keep it a
   plain `if (promoCode.isPresent())` branch or an `ifPresent`; never hide that inside `map`.
   One Optional, one terminal. Decide present or absent once, and give helpers the value, never
   the `Optional`: `attachment.map(Attachment::bytes).ifPresent(this::rejectOversize)`.

2. Match the API to the operation: `map` for transforms, `flatMap` for Optional-returning calls,
   `orElseGet` for non-trivial fallback work, and `orElseThrow` only when absence is an error. Keep
   fallback computation inside the supplier; don't assign or return it before checking the Optional.

   ```java
   Quote quoteFor(Source source, Request request) {   // source may be null
       return Optional.ofNullable(source)
           .map(Source::rawValue)
           .flatMap(this::parseValue)                   // Optional<Quote>
           .orElseGet(() -> computeFallback(request));
   }
   ```

3. Keep real streams readable. A lookup over a collection that yields zero or one element is
   `stream().filter(...).findAny()` consumed with `map`/`orElse`, not a loop with `break` or a
   null sentinel. Preserve `findFirst()` when an earlier element must win because the source is
   ordered. Use `findAny()` only when every match would do, as with a key that is unique in its
   collection. Flatten
   `Stream<Optional<T>>` with `flatMap(Optional::stream)` on Java 9+.
4. Bind selectors once.
   - Treat `Optional<Boolean>` as three states when absence differs from `false`.
   - Predicate-only presence checks are fine when the value isn't read.
   - Use `ifPresent` or Java 9+ `ifPresentOrElse` for side-effect boundaries.
   - Select from other owning containers with their fallback operation (`ScopedValue.orElse`,
     `Map.getOrDefault`) and act once on the result; the shapes are in
     [java-optional-api.md](references/java-optional-api.md).
5. Keep primitive Optionals primitive. Use `OptionalInt`, `OptionalLong`, or `OptionalDouble`
   directly; don't box or use `isPresent()` plus `getAsInt()`/`getAsLong()`/`getAsDouble()`.
6. Use a plain branch only at a real checked IO, prompt, checked parser, or null-based API boundary.
   Before checked prompts, select any non-IO Optional value first. At the checked branch, use the
   baseline-compatible empty-guard shape:

   ```java
   Optional<Printer> chosen = chosenPrinter(options);   // no IO in the selection
   // Java 11+; use !chosen.isPresent() on Java 8.
   if (chosen.isEmpty()) return promptForPrinter(console);   // the only checked branch
   // Checked fallback is handled above; read the present value once.
   return chosen.get();
   ```

   After such a guard the one read is `get()`; an `orElseThrow()` after the guard is a second
   presence decision.

7. In a review, keep the scope honest.
   - A proposal that changes a public record, accessor, parameter, or return type (a nullable
     field to `Optional`, `Optional` in a DTO or parameter) is an API change, not a local
     cleanup. Say so, keep the local code as it is, and ask for that redesign as its own change,
     reviewed for what it breaks.
   - Where `findFirst()` stays because the input is ordered, say that the order is the contract
     and describe a test that fails under `findAny()`, with several matches where the result
     must be the first of them.
   - Where `orElse(null)` stays, state why it may, which is that the type on the other side
     defines absence as `null`, so the Optional ends here.

     ```java
     return new LegacyTicket(id, note.orElse(null));   // LegacyTicket.note() is null when absent
     ```
8. Verify each changed branch. Run focused tests or trace present/absent/fallback cases. Confirm
   return values, exceptions, prompts, side effects, laziness, output, and branch order. Run the
   marker scan from [hard-stops.md](references/hard-stops.md); fix relevant hits and re-scan.
