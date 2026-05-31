# Eval Case Inventory

Maintainer-only inventory. Do not link this file from runtime skill references.

## Eval Scoring Rubric

A good eval output:

- preserves return values, exception types/messages, public output, prompts, branch order, side
  effects, and lazy/eager timing;
- avoids `orElse(null)` null-control-flow, fake single-Optional streams/lists, and ordinary
  presence-check/value-read replacements;
- distinguishes single Optional values from real collection streams;
- distinguishes fake single-Optional streams from real streams of Optional values that should use
  `flatMap(Optional::stream)`;
- distinguishes absence-as-error from fallback;
- distinguishes checked-exception boundaries from ordinary Optional control flow;
- stays readable to normal Java maintainers;
- doesn't introduce unnecessary helpers, dependencies, labels, or sentinel state;
- keeps `findFirst()` only where order matters and uses `findAny()` when all matches are equivalent;
- explains non-obvious choices for checked exceptions, nullable interop, and ordering when the
  requested output format allows prose.
- for review-only tasks, gives an explicit no-change decision and rationale instead of producing an
  empty answer.

## Eval Cases

### Eval 1: Replace `isPresent()` Plus `get()` Without Null

Input:

```java
import java.util.Optional;

final class UserService {
    String displayName(Optional<User> user) {
        if (user.isPresent()) {
            return user.get().displayName();
        }
        return "Anonymous";
    }

    record User(String displayName) {}
}
```

Expected:

```java
String displayName(Optional<User> user) {
    return user.map(User::displayName).orElse("Anonymous");
}
```

Reject `orElse(null)` and `optional.stream().toList()` rewrites.

### Eval 2: Preserve Lazy Side Effects

Input:

```java
import java.util.Optional;

final class WorkpadService {
    Result upsert(Optional<Comment> existing, String text) {
        if (existing.isPresent()) {
            return update(existing.get(), text);
        }
        return create(text);
    }

    Result update(Comment comment, String text) { return new Result("updated"); }
    Result create(String text) { return new Result("created"); }

    record Comment(String id) {}
    record Result(String status) {}
}
```

Expected:

```java
Result upsert(Optional<Comment> existing, String text) {
    return existing
            .map(comment -> update(comment, text))
            .orElseGet(() -> create(text));
}
```

Reject `orElse(create(text))` because it runs create eagerly.

### Eval 3: Keep Real Collection Stream

Input already-good code:

```java
import java.util.Optional;
import java.util.Set;

final class CommandRedactor {
    private static final Set<String> SECRET_OPTIONS = Set.of("--token", "--api-key");

    Optional<String> secretOption(String arg) {
        return SECRET_OPTIONS.stream()
                .filter(option -> arg.equals(option) || arg.startsWith(option + "="))
                .findAny();
    }
}
```

Expected: keep the stream and answer with a short review comment. Don't rewrite it to a manual loop
only because it returns Optional.

### Eval 4: Keep `findFirst()` When Order Matters

```java
import java.util.List;
import java.util.Optional;

final class RouteSelector {
    Optional<Route> firstEnabledRoute(List<Route> routes) {
        return routes.stream()
                .filter(Route::enabled)
                .findFirst();
    }

    record Route(String name, boolean enabled) {}
}
```

Expected: keep `findFirst()` because first enabled route is the priority contract.

### Eval 5: Use `findAny()` When Order Doesn't Matter

```java
import java.util.Optional;
import java.util.Set;

final class FlagMatcher {
    Optional<String> matchingFlag(Set<String> flags, String arg) {
        return flags.stream()
                .filter(flag -> arg.equals(flag) || arg.startsWith(flag + "="))
                .findFirst();
    }
}
```

Expected: use `findAny()` and include a one-sentence rationale that all matches are equivalent.

Explain briefly that a `Set` has no first-match priority contract here and any matching flag is
equivalent.

### Eval 6: Allow Plain Branching At Checked Boundaries

```java
import java.io.IOException;
import java.util.Optional;

final class WorkspaceSelector {
    String workspaceId(Options options, Terminal terminal) throws IOException {
        Optional<String> configured = options.workspaceId();
        if (configured.isPresent()) {
            return configured.get();
        }
        return promptForWorkspace(terminal);
    }

    String promptForWorkspace(Terminal terminal) throws IOException {
        return terminal.readLine("Workspace: ");
    }

    interface Options { Optional<String> workspaceId(); }
    interface Terminal { String readLine(String prompt) throws IOException; }
}
```

Expected: use an explicit `isEmpty()` branch, preserve `throws IOException`, and include a
one-sentence rationale for keeping plain branching at this checked-IO boundary. Don't introduce
unchecked wrappers or a checked-Optional helper.

### Eval 7: Recognize Absence-As-Error

```java
import java.util.Map;
import java.util.Optional;

final class ConfigLookup {
    String required(Map<String, String> values, String key) {
        Optional<String> value = Optional.ofNullable(values.get(key));
        if (value.isPresent()) {
            return value.get();
        }
        throw new IllegalArgumentException("Missing config: " + key);
    }
}
```

Expected:

```java
String required(Map<String, String> values, String key) {
    return Optional.ofNullable(values.get(key))
            .orElseThrow(() -> new IllegalArgumentException("Missing config: " + key));
}
```

### Eval 8: Isolate Nullable Interop

```java
import java.util.Optional;

final class LegacyAdapter {
    LegacyRequest toLegacy(Optional<String> comment) {
        return new LegacyRequest(comment.orElse(null));
    }

    record LegacyRequest(String nullableComment) {}
}
```

Expected: this can be acceptable if the legacy API genuinely uses `null` for absent. Don't create
extra null-control-flow branches around it.

If the surrounding API could be changed to avoid nullable interop, treat that as a separate
API/design decision. Don't bundle a record, DTO, serialization, or external contract change into a
local Optional cleanup without explicit scope.

### Eval 9: Avoid Repeated Reads After One Presence Check

Input:

```java
import java.util.Optional;

final class CardMover {
    Card moveIfNeeded(Optional<ListRef> target, Card card) {
        if (target.isEmpty()) {
            return card;
        }
        if (card.listId().equals(target.get().id())) {
            return card;
        }
        return new Card(card.id(), target.get().id());
    }

    record Card(String id, String listId) {}
    record ListRef(String id) {}
}
```

Preferred:

```java
Card moveIfNeeded(Optional<ListRef> target, Card card) {
    return target
            .map(list -> moveIfNeeded(list, card))
            .orElse(card);
}

private Card moveIfNeeded(ListRef target, Card card) {
    if (card.listId().equals(target.id())) {
        return card;
    }
    return new Card(card.id(), target.id());
}
```

Also acceptable when clearer at a checked or imperative boundary:

```java
Card moveIfNeeded(Optional<ListRef> target, Card card) {
    if (target.isEmpty()) {
        return card;
    }
    ListRef list = target.orElseThrow();
    if (card.listId().equals(list.id())) {
        return card;
    }
    return new Card(card.id(), list.id());
}
```

Reject repeated `target.get()` or repeated `target.orElseThrow()` after a single guard.

### Eval 10: Don't Turn One Optional Into A List Or Loop

Input:

```java
import java.util.Optional;

final class GreetingService {
    String greeting(Optional<String> name) {
        for (String value : name.stream().toList()) {
            return "Hello " + value;
        }
        return "Hello guest";
    }
}
```

Expected:

```java
String greeting(Optional<String> name) {
    return name.map(value -> "Hello " + value).orElse("Hello guest");
}
```

Reject loops over `optional.stream().toList()` when the source is one Optional, not a real
collection.

### Eval 10a: Flatten A Real Stream Of Optional Values

Input:

```java
import java.util.List;
import java.util.Map;
import java.util.Optional;

final class CatalogFeed {
    List<ProductCard> visibleCards(List<Map<String, Object>> payloads, StoreContext context) {
        return payloads.stream()
                .map(payload -> normalize(payload, context))
                .filter(Optional::isPresent)
                .map(Optional::get)
                .filter(card -> card.active() && !card.discontinued())
                .toList();
    }

    Optional<ProductCard> normalize(Map<String, Object> payload, StoreContext context) {
        return Optional.empty();
    }

    record StoreContext(List<String> activeCategoryIds) {}
    record ProductCard(String id, boolean active, boolean discontinued) {}
}
```

Expected:

```java
List<ProductCard> visibleCards(List<Map<String, Object>> payloads, StoreContext context) {
    return payloads.stream()
            .map(payload -> normalize(payload, context))
            .flatMap(Optional::stream)
            .filter(card -> card.active() && !card.discontinued())
            .toList();
}
```

Reject `filter(Optional::isPresent).map(Optional::get)` in a stream pipeline. Also reject treating
this as a fake single-Optional stream case; the source is a real collection of payloads.

### Eval 11: Write First-Pass Optional Code With Lazy Creation

Prompt:

```text
Write a Java method that returns an existing cached document if present. If it's absent, create a
document, store it in the cache, and return it.
```

Expected shape:

```java
Document document(String key) {
    return cache.find(key).orElseGet(() -> createAndStore(key));
}

private Document createAndStore(String key) {
    Document document = create(key);
    cache.put(key, document);
    return document;
}
```

Reject `isPresent()` plus `get()`, `orElse(createAndStore(key))`, and `optional.stream().toList()`.
The fallback mutates cache state, so it must stay lazy.

### Eval 12: Selector Optional Shouldn't Become Fake Collection Control Flow

Input:

```java
import java.nio.file.Path;
import java.util.List;
import java.util.Optional;

final class DiagnosticSelector {
    Selection select(Manifest manifest, Optional<String> board, Optional<Path> workflow, Path configDir) {
        if (board.isPresent() && workflow.isPresent()) {
            throw new IllegalArgumentException("--board and --workflow cannot be used together.");
        }
        if (board.isPresent()) {
            return byBoard(manifest, board.orElseThrow());
        }
        if (workflow.isPresent()) {
            return byWorkflow(manifest, workflow.orElseThrow(), configDir);
        }
        return new Selection("none", manifest.boards(), Optional.empty());
    }

    Selection byBoard(Manifest manifest, String board) { return new Selection("board", List.of(), Optional.empty()); }
    Selection byWorkflow(Manifest manifest, Path workflow, Path configDir) { return new Selection("workflow", List.of(), Optional.of(workflow)); }
    record Manifest(List<String> boards) {}
    record Selection(String kind, List<String> boards, Optional<Path> workflow) {}
}
```

Expected: keep the boolean-only conflict check, then use `board.map(...).orElseGet(...)` with a
nested workflow Optional boundary. Reject `orElse(null)` and `optional.stream().toList()` rewrites.

### Eval 13: Output Path Should Use A Side-Effect Boundary

Input:

```java
import java.nio.file.Path;
import java.util.Optional;

final class ReportCommand {
    void finish(Optional<Path> output, String report) {
        if (output.isPresent()) {
            write(output.orElseThrow(), report);
        } else {
            print(report);
        }
    }

    void write(Path path, String report) {}
    void print(String report) {}
}
```

Expected: use `output.ifPresentOrElse(path -> write(path, report), () -> print(report))`. Reject
null and fake collection workarounds.

### Eval 14: Reject `orElse(null)` As A Proposed Cleanup

Review a proposed change from `isPresent()` plus `get()` to `orElse(null)` plus `value != null`.

Expected: reject the proposal as nullable control flow in another form and suggest
`user.map(User::displayName).orElse("Anonymous")` or an equivalent direct Optional boundary.

### Eval 15: Reject Loop Overcorrection For A Real Collection Stream

Review a proposed rewrite from a readable `REDACTED_VALUE_OPTIONS.stream().filter(...).findAny()`
lookup to a manual loop.

Expected: reject the rewrite as unnecessary for this cleanup. The source is a real `Set`, not a
single Optional being forced through stream syntax, and `findAny()` is appropriate because any
matching redacted option is equivalent.

### Eval 16: Reject Local Checked-Optional Helper

Review a proposed `CheckedOptionals.mapOrElseGet(...)` helper that adapts `IOException` through
`UncheckedIOException` only to preserve fluent Optional syntax around a prompting fallback.

Expected: reject the helper-based local cleanup. Keep a narrow explicit branch at the checked-IO
boundary and don't add a functional dependency for this case.

### Eval 17: Write First-Pass Optional Formatting Code

Ask the agent to create an `AssigneeFormatter` class with `label(Optional<User> assignee)`.

Expected: use a direct Optional boundary such as `assignee.map(...).orElse("unassigned")`, return
`"@" + handle` when the present user's handle isn't blank, return `displayName()` for a present
user with a blank handle, and return `"unassigned"` when absent. Reject `isPresent()` plus `get()`,
`orElse(null)` plus null branching, and fake single-Optional collection/loop workarounds.

### Eval 18: Write First-Pass Selector Code

Ask the agent to create a diagnostics selector with optional board/workflow selectors and a
mutual-exclusion check.

Expected: keep the conflict check as boolean-only validation, then use direct Optional boundaries
for the value-reading board/workflow branches. Reject `get()`, `orElseThrow()`, null, and fake
collection/list unwrapping for selector values.

### Eval 19: Write First-Pass Redacted Option Matcher

Ask the agent to create a redacted command option matcher from a real `Set<String>`.

Expected: use a readable real collection lookup ending in `findAny()`. Reject null sentinels and do
not turn this into a single-Optional workaround.

### Eval 20: Review Legacy Null Boundary

Ask the agent to review an isolated `new AuditEvent(comment.orElse(null))` adapter.

Expected: allow it when the legacy record genuinely uses `null` for absence, avoid extra null
branching, and frame any API redesign as separate work.

### Eval 21: Review Optional DTO Overreach

Review a proposed cleanup that changes a legacy request record field from nullable `String` to
`Optional<String>`.

Expected: reject the bundled API/DTO change as out of scope for a local Optional cleanup.

### Eval 22: Review `findAny()` Order Regression

Review a proposed change from `findFirst()` to `findAny()` in a `primaryContact(List<Contact>)`
lookup.

Expected: reject the change because the method name and list order imply first-match priority.

### Eval 23: Write First-Pass Output Routing

Ask the agent to create a router that sends to an optional webhook or enqueues locally.

Expected: use `ifPresentOrElse` or an equivalent side-effect boundary, not `isPresent()` plus a value
read, null, or fake collection control flow.

### Eval 24: Write Priority Fallback Code

Ask the agent to create code that chooses an optional CLI workspace, then an optional environment
workspace, then a default workspace.

Expected: use `cli.or(() -> environment).orElse(defaultWorkspace)` or an equivalent direct Optional
priority boundary. Reject `isPresent()` plus `get()`, null sentinels, and fake collection loops.

### Eval 25: Review Single Optional Stream Loop

Review a proposed cleanup that turns a single `Optional<User>` into `assignee.stream().toList()` and
loops over it.

Expected: reject the proposal because it's a fake collection workaround. Suggest a direct
`assignee.map(...).orElse(...)` shape.

### Eval 26: Review Eager Fallback Regression

Review a proposed cleanup that changes a lazy creation branch to `orElse(createAndStore(key))`.

Expected: reject the proposal because creation and cache mutation would run eagerly. Suggest
`orElseGet(...)` or a named lazy helper.

### Eval 27: Review Null Error Workaround

Review a proposed cleanup that changes absence-as-error Optional code to `orElse(null)` plus a local
null check.

Expected: reject the proposal and keep `orElseThrow(...)` for the error boundary.

### Eval 28: Write Card Move Plan

Ask the agent to create code that returns the original card when an optional target list is absent
or already current, otherwise returns a moved card.

Expected: bind the target list once through `map` plus a helper, or another direct value-binding
boundary. Reject repeated `get()`, null, and fake collection control flow.

### Eval 29: Write Clean Label Code

Ask the agent to create a label from an optional raw string by trimming, filtering blanks, and using
a fallback.

Expected: use `map(String::trim).filter(...).orElse(...)` or equivalent. Reject `isPresent()` plus
`get()` and `orElse(null)` plus null branching.

### Eval 30: Review Repeated Get Cleanup

Review a proposed cleanup that preserves a guard followed by repeated `target.get()` calls.

Expected: request a direct value-binding shape or bind the selected value once; reject repeated
Optional reopening after the guard.

### Eval 31: Primitive Optional Side Effect

Ask the agent to improve `OptionalInt` handling in a loop that parses positive integer priority
labels and writes them into a map.

Expected: use `positiveInteger(value).ifPresent(priority -> values.put(..., priority))` or an
equivalent `OptionalInt` terminal. Reject `isPresent()` followed by `getAsInt()`.

### Eval 32: Tri-State Optional Boolean Mode

Ask the agent to improve a configurator that accepts `Optional<Boolean>` where `true`, `false`, and
empty each have different behavior.

Expected: keep explicit `false`, explicit `true`, and absent branches separate. Reject
`orElse(false)` before fallback logic and reject repeated `isPresent()` plus `orElseThrow()` value
reads.

### Eval 33: Predicate-Only Optional Check

Ask the agent to improve code that returns whether an optional session customer id equals an
expected id.

Expected: use `filter(...).isPresent()`, `map(...).orElse(false)`, or an equivalent predicate-only
Optional boundary. Reject `isPresent()` followed by `get()` or `orElseThrow()` just to compare the
value.
