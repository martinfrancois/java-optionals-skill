# Java Optionals Skill

Tessl-compatible agent skill for writing, reviewing, and refactoring Java `Optional` code.

The installable plugin name is:

```text
martinfrancois/java-optionals
```

The repository name is intentionally neutral:

```text
java-optionals-skill
```

## Purpose

This skill helps agents keep `Optional` as a clear present/absent boundary without turning it back
into null control flow, fake collections, or unreadable fluent code. It focuses on observed failure
modes from real Java refactors:

- `isPresent()` or `isEmpty()` followed by immediate value reads;
- `orElse(null)` followed by local null branching;
- converting one Optional into a stream/list only to avoid a branch;
- replacing readable real collection streams with worse loops;
- using `findFirst()` when encounter order does not matter;
- hiding checked exceptions only to preserve fluent Optional syntax;
- confusing boolean-only Optional validation with value-reading selector branches;
- using presence checks plus value reads where `ifPresentOrElse` would express side-effect branches;
- adding broad functional dependencies for narrow local cleanups.

## Layout

```text
skills/java-optionals/
├── SKILL.md
├── agents/openai.yaml
├── evals/evals.json
└── references/
    ├── optional-examples.md
    └── source-notes.md
```

## Validation

Run the local structural checks:

```bash
python3 /root/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/java-optionals
tessl plugin lint .
tessl plugin pack .
```

This repository includes both `.tessl-plugin/plugin.json` and `tile.json` while the local Tessl CLI
is in transition between tile and plugin packaging paths. `plugin.json` is authoritative; `tile.json`
exists so older pack/info paths can still package the repository.

Run evals when authenticated with Tessl:

```bash
tessl project create --workspace martinfrancois java-optionals-skill
tessl eval run --variant with-context --variant without-context .
```

Current benchmark run:

- Run ID: `019e75e0-02e8-7439-bda2-105a036b3812`
- Benchmark content commit: `e420bb7`
- Baseline: `255 / 336` (`75.9%`)
- With `java-optionals`: `336 / 336` (`100.0%`)
- Lift: `+81 / 336`, or `+24.1` percentage points

The hosted suite keeps lightweight smoke coverage for straightforward refactors, but weights the
benchmark toward the skill-specific failure modes: null-control-flow substitutions, real collection
stream overcorrection, checked-IO Optional boundaries, nullable interop, first-pass Optional code
writing, and `findFirst()` / `findAny()` intent.

## OSS Readiness

Before making this repository public:

- run the validation commands above;
- run the portable evals in `skills/java-optionals/evals/evals.json`;
- test the skill against at least one Java Optional refactor outside the source repository;
- run the `symphony-trello` fixture from the parent of
  `4aaa1a6e61572a932153578d3e48bb6a2923b0cf` as a validation set, not as training data;
- confirm the skill is self-contained and does not require the original issue, gist, fixture repo,
  or external articles to operate.

## Provenance

The skill was distilled from `martin-francois/symphony-trello` issue 96 and every issue comment
present at creation time. See `skills/java-optionals/references/source-notes.md` for maintenance
notes and source treatment.
