# Java Optional Examples And Eval Cases

Use these examples for non-trivial Optional refactors and to evaluate whether an agent applies the
`java-optionals` skill correctly.

## Table Of Contents

- [Observed Production Failure Patterns](#observed-production-failure-patterns)
- [Iteration Histories](#iteration-histories)
- [Eval Scoring Rubric](#eval-scoring-rubric)
- [Eval Cases](#eval-cases)

## Observed Production Failure Patterns

The skill guards against patterns agents have actually written or preserved in production Java code:

- `existing.isPresent()` followed by `existing.get()` in an update-or-create flow. The final shape
  used `findFirst().map(...).orElseGet(...)` with named update/create helpers so the create branch
  stayed lazy.
- `target.isEmpty()` followed by repeated `target.get()` reads after a successful guard. The final
  shape bound the selected value once before using it.
- `options.workspaceId().isPresent()` followed by `options.workspaceId().orElseThrow()` before a
  prompting fallback. The final shape kept a narrow explicit branch because the fallback performs
  checked IO.
- `frontMatter.isEmpty()` followed by multiple `frontMatter.get()` reads. The final shape moved the
  map access into a helper or Optional boundary so the value was not repeatedly reopened.
- `optional.orElse(null)` in mixed contexts. Some instances were acceptable nullable interop with an
  existing record or API boundary; others invited local null-control-flow branching.
- A real collection stream ending in an Optional result was first handled with
  `isPresent()`/`orElseThrow()`, then overcorrected into a loop. The final shape kept the readable
  collection stream and handled the Optional result directly.

## Iteration Histories

### 1. Upsert Should Use Optional As The Decision Boundary

Starting point:

```java
import java.util.List;
import java.util.Optional;

final class WorkpadService {
    Result upsertWorkpad(Card card, String text) {
        Optional<Comment> existing = card.comments().stream()
                .filter(this::isWorkpadComment)
                .findFirst();

        if (existing.isPresent()) {
            Comment workpad = existing.get();
            if (workpad.id() == null || workpad.id().isBlank()) {
                return Result.failure("missing_action_id");
            }
            return updateExistingWorkpad(workpad, text);
        }

        if (card.comments().size() >= 1000) {
            return Result.failure("comment_window_incomplete");
        }
        return createWorkpad(card, text);
    }

    boolean isWorkpadComment(Comment comment) {
        return comment.text() != null && comment.text().startsWith("<!-- workpad -->");
    }

    Result updateExistingWorkpad(Comment workpad, String text) { return Result.success("updated"); }
    Result createWorkpad(Card card, String text) { return Result.success("created"); }

    record Card(List<Comment> comments) {}
    record Comment(String id, String text) {}
    record Result(boolean ok, String status) {
        static Result success(String status) { return new Result(true, status); }
        static Result failure(String status) { return new Result(false, status); }
    }
}
```

Bad attempted fix:

```java
Comment workpad = card.comments().stream()
        .filter(this::isWorkpadComment)
        .findFirst()
        .orElse(null);

if (workpad != null) {
    return updateExistingWorkpad(workpad, text);
}
return createWorkpad(card, text);
```

Better final shape:

```java
Result upsertWorkpad(Card card, String text) {
    return card.comments().stream()
            .filter(this::isWorkpadComment)
            .findFirst()
            .map(workpad -> updateExistingWorkpad(card, workpad, text))
            .orElseGet(() -> createWorkpad(card, text));
}

private Result updateExistingWorkpad(Card card, Comment workpad, String text) {
    if (workpad.id() == null || workpad.id().isBlank()) {
        return Result.failure("missing_action_id");
    }
    return Result.success("updated");
}

private Result createWorkpad(Card card, String text) {
    if (card.comments().size() >= 1000) {
        return Result.failure("comment_window_incomplete");
    }
    return Result.success("created");
}
```

Why good: the Optional remains the update-or-create boundary, and `orElseGet(...)` keeps create
lazy.

### 2. Real Collection Stream Should Not Become A Labeled Loop

Starting point:

```java
import java.util.Optional;
import java.util.Set;

final class CommandRedactor {
    private static final Set<String> SECRET_OPTIONS = Set.of("--token", "--api-key");

    Optional<String> secretOption(String arg) {
        return SECRET_OPTIONS.stream()
                .filter(option -> arg.equals(option) || arg.startsWith(option + "="))
                .findFirst();
    }
}
```

Bad attempted fix:

```java
arguments:
for (String arg : args) {
    for (String option : SECRET_OPTIONS) {
        if (arg.equals(option)) {
            redactNext = true;
            continue arguments;
        }
        if (arg.startsWith(option + "=")) {
            sanitizedArgs.add(option + "=<redacted>");
            continue arguments;
        }
    }
    sanitizedArgs.add(arg);
}
```

Better final shape:

```java
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.Set;

final class CommandRedactor {
    private static final Set<String> SECRET_OPTIONS = Set.of("--token", "--api-key");

    private static Optional<String> secretOption(String arg) {
        return SECRET_OPTIONS.stream()
                .filter(option -> arg.equals(option) || arg.startsWith(option + "="))
                .findAny();
    }

    String sanitizeCommand(List<String> args) {
        List<String> sanitizedArgs = new ArrayList<>();
        boolean redactNext = false;

        for (String arg : args) {
            if (redactNext) {
                sanitizedArgs.add("<redacted>");
                redactNext = false;
            } else {
                Optional<String> option = secretOption(arg);
                sanitizedArgs.add(option
                        .map(match -> arg.equals(match) ? arg : match + "=<redacted>")
                        .orElse(arg));
                redactNext = option.map(arg::equals).orElse(false);
            }
        }

        return String.join(" ", sanitizedArgs);
    }
}
```

Why good: matching is centralized in a real collection stream, `findAny()` is correct because any
match is equivalent, and the remaining loop only tracks real sequence state.

### 3. Checked Prompting Fallback Should Use Plain Branching

Starting point:

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

Rejected helper approach:

```java
return CheckedOptionals.mapOrElseGet(
        options.workspaceId(),
        id -> id,
        () -> promptForWorkspace(terminal));
```

Rejected helper internals:

```java
import java.io.IOException;
import java.io.UncheckedIOException;
import java.util.Optional;
import java.util.function.Function;

final class CheckedOptionals {
    static <T, R> R mapOrElseGet(Optional<T> value, Function<T, R> present, CheckedSupplier<R> absent)
            throws IOException {
        try {
            return value.map(present).orElseGet(() -> unchecked(absent));
        } catch (UncheckedIOException e) {
            throw e.getCause();
        }
    }

    private static <R> R unchecked(CheckedSupplier<R> supplier) {
        try {
            return supplier.get();
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }

    @FunctionalInterface
    interface CheckedSupplier<T> {
        T get() throws IOException;
    }
}
```

Better final shape:

```java
import java.io.IOException;
import java.util.Optional;

final class WorkspaceSelector {
    String workspaceId(Options options, Terminal terminal) throws IOException {
        Optional<String> configured = options.workspaceId();
        if (configured.isEmpty()) {
            return promptForWorkspace(terminal);
        }
        return configured.orElseThrow();
    }

    String promptForWorkspace(Terminal terminal) throws IOException {
        return terminal.readLine("Workspace: ");
    }

    interface Options { Optional<String> workspaceId(); }
    interface Terminal { String readLine(String prompt) throws IOException; }
}
```

Why good: the checked exception remains visible, and the branch is a narrow checked-IO boundary.

### 4. Functional Library Decisions Are Separate Design Work

Attractive Vavr-style shape:

```java
import io.vavr.control.Option;
import java.io.IOException;
import java.util.Optional;

final class WorkspaceSelector {
    String workspaceId(Options options, Terminal terminal) throws IOException {
        return Option.ofOptional(options.workspaceId())
                .map(id -> id)
                .getOrElseTry(() -> promptForWorkspace(terminal));
    }

    String promptForWorkspace(Terminal terminal) throws IOException {
        return terminal.readLine("Workspace: ");
    }

    interface Options { Optional<String> workspaceId(); }
    interface Terminal { String readLine(String prompt) throws IOException; }
}
```

Why not as a local cleanup: it introduces a second Optional-like type and a broader repository style
decision. Evaluate that separately instead of adding a dependency for a few call sites.

### 5. Selector And Output Optionals Need Different Boundaries

Starting selector code:

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

Bad attempted fix:

```java
List<String> boards = board.stream().toList();
if (!boards.isEmpty()) {
    return byBoard(manifest, boards.getFirst());
}
```

Better final shape:

```java
Selection select(Manifest manifest, Optional<String> board, Optional<Path> workflow, Path configDir) {
    if (board.isPresent() && workflow.isPresent()) {
        throw new IllegalArgumentException("--board and --workflow cannot be used together.");
    }
    return board
            .map(selector -> byBoard(manifest, selector))
            .orElseGet(() -> workflow
                    .map(path -> byWorkflow(manifest, path, configDir))
                    .orElseGet(() -> new Selection("none", manifest.boards(), Optional.empty())));
}
```

Why good: the mutual-exclusion check stays a boolean-only presence check, but each value-reading
branch uses the Optional as the selector boundary. The no-selector branch stays lazy, and no fake
collection or null workaround is introduced.

Related output-sink starting code:

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

Better final shape:

```java
void finish(Optional<Path> output, String report) {
    output.ifPresentOrElse(
            path -> write(path, report),
            () -> print(report));
}
```

Why good: the Optional directly chooses between two side-effect branches. If either branch has
checked-exception friction, reconsider whether explicit branching is clearer.

## Eval Scoring Rubric

A good eval output:

- preserves return values, exception types/messages, public output, prompts, branch order, side
  effects, and lazy/eager timing;
- avoids `orElse(null)` null-control-flow, fake single-Optional streams/lists, and ordinary
  presence-check/value-read replacements;
- distinguishes single Optional values from real collection streams;
- distinguishes absence-as-error from fallback;
- distinguishes checked-exception boundaries from ordinary Optional control flow;
- stays readable to normal Java maintainers;
- does not introduce unnecessary helpers, dependencies, labels, or sentinel state;
- keeps `findFirst()` only where order matters and uses `findAny()` when all matches are equivalent;
- explains non-obvious choices for checked exceptions, nullable interop, and ordering when the
  requested output format allows prose;
- follows explicit output instructions, such as returning code followed by a short rationale or
  caveat when requested;
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

Expected: keep the stream and answer with a short review comment. Do not rewrite it to a manual loop
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

### Eval 5: Use `findAny()` When Order Does Not Matter

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

Expected: use `findAny()` and then include a one-sentence rationale that all matches are equivalent.

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
one-sentence rationale for keeping plain branching at this checked-IO boundary. Do not introduce
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

Expected: this can be acceptable if the legacy API genuinely uses `null` for absent. Do not create
extra null-control-flow branches around it.

If the surrounding API could be changed to avoid nullable interop, treat that as a separate
API/design decision. Do not bundle a record, DTO, serialization, or external contract change into a
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

### Eval 10: Do Not Turn One Optional Into A List Or Loop

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

### Eval 11: Write First-Pass Optional Code With Lazy Creation

Prompt:

```text
Write a Java method that returns an existing cached document if present. If it is absent, create a
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

### Eval 12: Selector Optional Should Not Become Fake Collection Control Flow

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

Expected: use `output.ifPresentOrElse(path -> write(path, report), () -> print(report))`, then
include a short checked-exception caveat unless the requested output is code-only. Reject null and
fake collection workarounds.
