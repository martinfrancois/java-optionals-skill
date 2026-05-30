# Java Optionals

AI agents often know enough Java to reach for `Optional`, but not enough to use it well.

They write code that looks modern at first glance, then leaves you with `isPresent()` plus `get()`,
`orElse(null)`, fallback code that runs too early, fake one-item lists, or a clear stream rewritten
as a noisy loop.

This skill gives the agent a small decision guide before it writes or changes Optional code: choose
the Optional shape, keep fallback work lazy, keep real collection streams readable, and use a plain
branch when checked IO makes that clearer.

## Contents

- [Getting Started](#getting-started)
- [Why This Exists](#why-this-exists)
- [What Good Looks Like](#what-good-looks-like)
- [What It Helps With](#what-it-helps-with)
- [Examples](#examples)
- [Benchmark](#benchmark)
- [Contributing](#contributing)
- [Provenance](#provenance)
- [License](#license)

## Getting Started

Install the skill:

```bash
tessl install github:martinfrancois/java-optionals-skill --skill java-optionals
```

Then ask the agent to use it:

```text
Use $java-optionals to implement this Java feature with Optional best practices.
```

For refactors:

```text
Use $java-optionals to refactor this Java method without changing its outputs or error handling.
```

For reviews:

```text
Use $java-optionals to review this proposed Optional cleanup. Create review.md with a decision and
rationale.
```

For focused first-pass Optional code:

```text
Use $java-optionals to write the first-pass implementation for this Java Optional fallback.
```

Install globally instead of into the current project:

```bash
tessl install --global github:martinfrancois/java-optionals-skill --skill java-optionals
```

If the skill is published in your Tessl workspace, you can also install it by package name:

```bash
tessl install martinfrancois/java-optionals
```

## Why This Exists

Use this skill when an agent writes or changes Java code that uses `Optional`.

When changing existing code, it helps the agent avoid accidental changes to results, errors, prompts,
side effects, and when fallback code runs.

The motivation was real AI-written Java code. The agent already used `Optional`, but often used it
in weak shapes. Then, when asked to clean up the code and follow Optional best practices, it sometimes
fixed one antipattern by adding a different one:

- replacing `isPresent()` / `get()` with `orElse(null)` and local null checks;
- using `isPresent()` or `isEmpty()` and then reading the same value with `get()` or
  `orElseThrow()`;
- losing laziness by using `orElse(...)` where `orElseGet(...)` is required;
- turning one optional value into a fake list, then reading the first item;
- replacing a clear collection stream with a long manual loop;
- hiding checked IO or user prompts behind clever helper code;
- changing the meaning of `findFirst()` / `findAny()` by accident.

For example, one cleanup changed a direct Optional selector into a fake list:

```java
// from
return selectedBoard
        .map(board -> selectBoardDiagnostics(manifest, board))
        .orElseGet(() -> selectDefaultDiagnostics(manifest));

// to
List<String> boards = selectedBoard.stream().toList();
if (!boards.isEmpty()) {
    return selectBoardDiagnostics(manifest, boards.getFirst());
}
```

Another changed a lazy Optional fallback into local null control flow:

```java
// from
return existingWorkpad
        .map(workpad -> updateExistingWorkpad(workpad, text))
        .orElseGet(() -> createWorkpad(card, text));

// to
Comment workpad = existingWorkpad.orElse(null);
if (workpad != null) {
    return updateExistingWorkpad(workpad, text);
}
```

And another changed a real option-set lookup into a harder-to-read loop:

```java
// from
return REDACTED_VALUE_OPTIONS.stream()
        .filter(option -> arg.equals(option) || arg.startsWith(option + "="))
        .findAny();

// to
arguments:
for (String arg : args) {
    for (String option : REDACTED_VALUE_OPTIONS) {
        if (arg.startsWith(option + "=")) {
            sanitized.add(option + "=<redacted>");
            continue arguments;
        }
    }
}
```

The goal is not to force every branch into a fluent chain. The goal is simpler: understand what the
`Optional` is doing, keep the important effects in the same places, and choose the clearest code.

## What Good Looks Like

Without this skill, agents may "clean up" Optional code but still leave the same control-flow
problem:

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

With this skill, the agent is pushed toward using the `Optional` for the actual decision and keeping
the create path lazy:

```java
Result upsertWorkpad(Card card, String text) {
    return card.comments().stream()
            .filter(this::isWorkpadComment)
            .findFirst()
            .map(workpad -> updateExistingWorkpad(card, workpad, text))
            .orElseGet(() -> createWorkpad(card, text));
}
```

## What It Helps With

Good fit:

- replacing `isPresent()` or `isEmpty()` followed by `get()` or `orElseThrow()`;
- avoiding `orElse(null)` followed by local null checks;
- choosing between `orElse(...)` and `orElseGet(...)`;
- keeping checked exceptions, user prompts, IO, and side effects in the right place;
- deciding whether `findFirst()` or `findAny()` keeps the same result;
- keeping real collection streams instead of rewriting them as noisy loops;
- avoiding `optional.stream().toList()` loops for a single `Optional`;
- handling old APIs that really use `null` for missing values;
- writing first-pass Optional code directly instead of cleaning up branchy code later.

Poor fit:

- broad Java style enforcement unrelated to `Optional`;
- large API redesigns, DTO changes, or new dependencies without maintainer agreement;
- changing business semantics just to make code look more functional;
- replacing every readable branch with a fluent chain.

## Examples

Simple fallback:

```java
String displayName(Optional<User> user) {
    return user.map(User::displayName).orElse("Anonymous");
}
```

Lazy creation or side effects:

```java
Document document(String key) {
    return cache.find(key).orElseGet(() -> createAndStore(key));
}
```

Side-effect branch:

```java
void finish(Optional<Path> output, String report) {
    output.ifPresentOrElse(
            path -> write(path, report),
            () -> print(report));
}
```

Checked IO case where a plain branch is clearer:

```java
String workspaceId(Options options, Terminal terminal) throws IOException {
    Optional<String> configured = options.workspaceId();
    if (configured.isEmpty()) {
        return promptForWorkspace(terminal);
    }
    return configured.orElseThrow();
}
```

Real collection lookup:

```java
private static Optional<String> redactedOption(String arg) {
    return REDACTED_VALUE_OPTIONS.stream()
            .filter(option -> arg.equals(option) || arg.startsWith(option + "="))
            .findAny();
}
```

## Benchmark

Current hosted benchmark:

- Run ID: `019e7611-55fd-717e-80bd-e9446d5ad34b`
- Benchmark content commit: `d267f22`
- Baseline: `276 / 616` (`44.8%`)
- With `java-optionals`: `616 / 616` (`100.0%`)
- Lift: `+340 / 616`, or `+55.2` percentage points
- Raw score ratio: `2.23x`
- Error reduction: `340 / 340` baseline missed points (`100.0%`)

The main benchmark is focused on implementation because the motivating failures happened during
normal AI-assisted Java changes, not only during code review. The scenarios start from branchy code,
ask for feature work, and score both the required outputs/effects and the Optional cleanup this skill
is meant to improve.

The broader review scenarios remain in `evals-reference/`. They are useful while developing the
skill, but many are small snippets that a strong generic model can already solve without the skill.

## Contributing

Want to improve the skill, evals, or package metadata? See [CONTRIBUTING.md](CONTRIBUTING.md).

## Provenance

This skill is based on real-world failures where coding agents changed Java `Optional` code into
different bad shapes while working on production-style tasks. The motivating discussion is
[`martin-francois/symphony-trello#96`](https://github.com/martin-francois/symphony-trello/issues/96).

The skill is self-contained: using it does not require access to that issue, the original repository,
development drafts, or any external article.

## License

MIT. See [LICENSE](LICENSE).
