# Java Optionals

Tessl tile for writing, reviewing, and refactoring Java `Optional` code without turning absence
handling into null control flow, fake collections, or over-clever fluent code.

```text
martinfrancois/java-optionals
```

## Why This Exists

`Optional` cleanup is easy to get wrong in agent-written Java code. A model may remove one smell and
replace it with another: `orElse(null)` plus null checks, loops over `optional.stream().toList()`,
eager fallbacks, unnecessary helper abstractions for checked exceptions, or loop rewrites that make a
real collection stream harder to read.

This tile gives agents a compact decision procedure for classifying the Optional shape first, then
choosing the clearest Java boundary while preserving behavior, exception contracts, public output,
laziness, and readability.

## Install

Install directly from GitHub:

```bash
tessl install github:martinfrancois/java-optionals-skill --skill java-optionals
```

Install globally instead of into the current project:

```bash
tessl install --global github:martinfrancois/java-optionals-skill --skill java-optionals
```

If the tile is published in your Tessl registry workspace, you can also install it by package name:

```bash
tessl install martinfrancois/java-optionals
```

## Use

Mention the skill when Optional handling matters:

```text
Use $java-optionals to refactor this Java method without changing behavior.
```

```text
Use $java-optionals to review this proposed Optional cleanup. Create review.md with a decision and
rationale.
```

```text
Use $java-optionals to write the first-pass implementation for this Java Optional fallback.
```

## What It Helps With

Good fit:

- replacing `isPresent()` or `isEmpty()` followed by `get()` or `orElseThrow()`;
- avoiding `orElse(null)` followed by local null checks;
- choosing between `orElse(...)` and `orElseGet(...)`;
- preserving checked-exception, prompting, IO, and side-effect boundaries;
- deciding whether `findFirst()` or `findAny()` preserves behavior;
- keeping real collection streams instead of rewriting them into noisy loops;
- avoiding `optional.stream().toList()` loops for a single `Optional`;
- handling legacy APIs that genuinely use `null` for absent values;
- writing first-pass Optional code directly instead of cleaning up branchy code later.

Poor fit:

- broad Java style enforcement unrelated to `Optional`;
- repository-wide API redesigns, DTO changes, or dependency additions without maintainer buy-in;
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

Checked IO boundary where plain branching is clearer:

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

## Repository Layout

```text
.
├── .tessl-plugin/plugin.json
├── evals/
├── evals-reference/
├── skills/java-optionals/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── evals/evals.json
│   └── references/
│       ├── optional-examples.md
│       └── source-notes.md
├── LICENSE
└── README.md
```

- `skills/java-optionals/SKILL.md` is the runtime instruction file loaded by agents.
- `skills/java-optionals/agents/openai.yaml` provides display metadata.
- `skills/java-optionals/references/optional-examples.md` contains non-trivial examples and eval
  case notes.
- `skills/java-optionals/references/source-notes.md` records provenance and maintenance decisions.
- `evals/` contains the hosted Tessl implementation-regression benchmark.
- `evals-reference/` keeps broader smoke, review, and exploratory scenarios that are useful during
  development but are not part of the headline benchmark.

## Benchmark

Current hosted benchmark:

- Run ID: `019e7611-55fd-717e-80bd-e9446d5ad34b`
- Benchmark content commit: `d267f22`
- Baseline: `276 / 616` (`44.8%`)
- With `java-optionals`: `616 / 616` (`100.0%`)
- Lift: `+340 / 616`, or `+55.2` percentage points
- Raw score ratio: `2.23x`
- Error reduction: `340 / 340` baseline missed points (`100.0%`)

The headline benchmark is implementation-focused because the motivating failures happened during
ordinary AI-assisted Java changes, not only during review-only tasks. The scenarios start from
branchy implementation code, ask for feature work, and score both behavior preservation and the
Optional cleanup this tile is meant to improve.

The broader smoke and review scenarios remain in `evals-reference/`. They are useful for developing
the skill, but they overstate baseline quality as a headline benchmark because many are small
isolated snippets that a strong generic model can already solve without the tile.

## Development

Validate the skill and package metadata:

```bash
python3 /root/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/java-optionals
tessl plugin lint .
tessl plugin pack .
```

Run hosted evals when authenticated with Tessl:

```bash
tessl project create --workspace martinfrancois java-optionals-skill
tessl eval run --variant with-context --variant without-context .
```

This repository includes both `.tessl-plugin/plugin.json` and `tile.json` while the local Tessl CLI
is in transition between tile and plugin packaging paths. `plugin.json` is authoritative; `tile.json`
exists so older pack/info paths can still package the repository.

Before cutting a public release, rerun validation and hosted evals, update the benchmark section, and
check the skill against at least one Java Optional change outside the source repository.

## Provenance

The skill was distilled from observed Java Optional cleanup failures captured in
`martin-francois/symphony-trello` issue 96 and its comments. The tile is self-contained: using it
does not require access to that issue, the original repository, the development gist, or any external
article.

## License

MIT. See [LICENSE](LICENSE).
