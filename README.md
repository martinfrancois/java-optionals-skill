# Java Optionals

Tessl tile for writing, reviewing, and refactoring Java `Optional` code without turning absence
handling into null control flow, fake collections, or over-clever fluent code.

```text
martinfrancois/java-optionals
```

The repository is named `java-optionals-skill`; the installable tile is `java-optionals`.

## What It Helps With

Use this tile when an agent is working on Java code that introduces, reviews, or changes
`Optional`, especially around:

- `isPresent()` or `isEmpty()` followed by `get()` or `orElseThrow()`;
- `orElse(null)` followed by local null checks;
- choosing between `orElse(...)` and `orElseGet(...)`;
- deciding whether `findFirst()` or `findAny()` preserves behavior;
- keeping real collection streams instead of rewriting them into noisy loops;
- avoiding `optional.stream().toList()` loops for a single `Optional`;
- preserving checked-exception, prompting, IO, and side-effect boundaries;
- handling legacy APIs that genuinely use `null` for absent values;
- writing first-pass Optional code directly instead of cleaning up branchy code later.

The goal is not to make every Optional chain fluent. The tile pushes agents to classify the
Optional shape first, then choose the clearest boundary while preserving behavior, public output,
exception contracts, laziness, and readability.

## Install

Install from the Tessl registry when the tile is available to your workspace:

```bash
tessl install martinfrancois/java-optionals
```

Install globally instead of into the current project:

```bash
tessl install --global martinfrancois/java-optionals
```

Install from this GitHub repository:

```bash
tessl install github:martinfrancois/java-optionals-skill --skill java-optionals
```

This repository is currently private. After it is made public, the GitHub install form should work
for users with normal repository access.

## Use

Mention the skill in prompts where Optional handling matters:

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

Good fit:

- local refactors that replace presence-check/value-read code with a clearer Optional boundary;
- review comments on proposed Optional cleanups;
- first-pass implementation of fallback, selector, and side-effect branches;
- checking whether an apparent Optional antipattern is actually a legacy or checked-IO boundary.

Poor fit:

- broad Java style enforcement unrelated to `Optional`;
- repository-wide API redesigns, DTO changes, or dependency additions without maintainer buy-in;
- changing business semantics just to make code look more functional.

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

## Included Files

```text
skills/java-optionals/
├── SKILL.md
├── agents/openai.yaml
├── evals/evals.json
└── references/
    ├── optional-examples.md
    └── source-notes.md
```

- `SKILL.md` is the runtime instruction file loaded by agents.
- `agents/openai.yaml` provides display metadata.
- `references/optional-examples.md` contains non-trivial examples and eval case notes.
- `references/source-notes.md` records provenance and maintenance decisions.
- `evals/` contains the hosted Tessl implementation-regression scenarios.
- `evals-reference/` keeps broader smoke, review, and exploratory scenarios that are useful during
  development but are not part of the headline hosted benchmark.

## Benchmark

Current hosted benchmark:

- Run ID: `019e7611-55fd-717e-80bd-e9446d5ad34b`
- Benchmark content commit: `d267f22`
- Baseline: `276 / 616` (`44.8%`)
- With `java-optionals`: `616 / 616` (`100.0%`)
- Lift: `+340 / 616`, or `+55.2` percentage points
- Raw score ratio: `2.23x`
- Error reduction: `340 / 340` baseline missed points (`100.0%`)

The headline hosted suite is intentionally implementation-focused because the motivating issue was
about AI-written or AI-preserved Optional antipatterns during normal code changes, not only review
comments. The scenarios start from branchy implementation code, ask for feature work, and score both
behavior preservation and the Optional cleanup that the skill is supposed to improve.

The broader smoke/review scenarios are preserved in `evals-reference/`. They are useful for
developing the skill, but they overstate baseline quality as a headline benchmark because many are
small isolated snippets that a strong generic model already solves without the tile.

## Validate Locally

Run structural checks:

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

## OSS Readiness

Before making this repository public:

- run the validation commands above;
- run the hosted eval suite and update the benchmark section;
- test the skill against at least one Java Optional refactor outside the source repository;
- confirm the tile is self-contained and does not require the original issue, gist, fixture repo, or
  external articles to operate;
- decide whether the package should remain under `martinfrancois/java-optionals`.

## Provenance

The skill was distilled from `martin-francois/symphony-trello` issue 96 and every issue comment
present at creation time. See `skills/java-optionals/references/source-notes.md` for maintenance
notes and source treatment.

## License

MIT.
