# Contributing

Thanks for helping improve Java Optionals. This project is a Tessl-compatible skill for guiding AI
agents toward better Java `Optional` usage.

Keep changes focused on the observed failure modes: weak Optional boundaries, null-style control
flow, fake single-Optional collections, eager fallback work, unclear checked-IO handling,
`findFirst()` / `findAny()` mistakes, and overcorrected collection streams.

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
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

- `skills/java-optionals/SKILL.md` is the runtime instruction file loaded by agents.
- `skills/java-optionals/agents/openai.yaml` provides display metadata.
- `skills/java-optionals/references/optional-examples.md` contains larger examples and eval case
  notes.
- `skills/java-optionals/references/source-notes.md` records where the skill came from and why it
  changed over time.
- `evals/` contains the hosted Tessl implementation-regression benchmark used for the headline
  README score.
- `evals-reference/` keeps extra review and test scenarios that are useful during development but
  are not part of the headline benchmark.

## Local Checks

Run these before committing skill, eval, README, or package changes:

```bash
python3 /root/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/java-optionals
tessl plugin lint .
tessl plugin publish --dry-run --skip-evals .
```

Also validate eval criteria JSON when editing evals:

```bash
find evals -name criteria.json -print0 | xargs -0 -n1 jq empty
```

## Hosted Evals

When authenticated with Tessl, run hosted evals before updating benchmark numbers:

```bash
tessl project create --workspace martinfrancois java-optionals-skill
tessl eval run --variant with-context --variant without-context .
```

The headline benchmark should stay focused on implementation tasks that mirror the motivating
failures. Broad review and smoke scenarios can live in `evals-reference/` unless they are part of the
headline measurement.

## Benchmark Updates

When the hosted benchmark changes:

- record the run ID;
- record the content commit;
- update baseline and skill scores;
- update lift, raw score ratio, and missed-point reduction;
- keep the README wording clear about what the benchmark measures.

## Release Checklist

Before publishing a public release:

- run local checks;
- run hosted evals or confirm the current benchmark is still valid;
- test the skill against at least one Java Optional change outside this repository;
- confirm `README.md` stays user-focused;
- confirm contributor-only process details live here.
