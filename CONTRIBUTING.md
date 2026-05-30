# Contributing

Thanks for helping improve the Java Optional Skill. This project is a Tessl-compatible skill for
guiding AI agents toward better Java `Optional` usage.

Keep changes focused on the observed failure modes: weak Optional boundaries, null-style control
flow, fake single-Optional collections, eager fallback work, unclear checked-IO handling,
`findFirst()` / `findAny()` mistakes, and overcorrected collection streams.

## Repository Layout

```text
.
├── .tessl-plugin/plugin.json
├── .github/workflows/
├── evals/
├── evals-reference/
├── scripts/
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
  aren't part of the headline benchmark.
- `scripts/` contains portable validation checks used by CI.
- `.github/workflows/ci.yml` validates skill metadata, eval criteria, Tessl linting, and the
  publish dry-run when `TESSL_TOKEN` is configured.
- `.github/workflows/skill-review.yml` runs `tessl skill review` on pull requests when
  `TESSL_TOKEN` is configured.

## Local Checks

Run these before committing skill, eval, README, package, script, or CI changes:

```bash
python3 scripts/validate_skill.py skills/java-optionals
python3 scripts/validate_eval_criteria.py evals evals-reference
tessl plugin lint .
```

Before a maintainer publishes, also run the Tessl publish dry-run:

```bash
bash scripts/check_publish_dry_run.sh .
```

That dry-run may fail because the current version already exists in the registry. That's expected
after a version has already been published; any other failure needs investigation.

## Commit Messages

Pull request titles and commits must use Conventional Commits, for example:

```text
feat: add selector fallback guidance
fix: preserve lazy Optional fallback
docs: clarify README motivation
ci: update release workflow
```

Release Please uses those commit types to decide the next version and generate release notes.

## Hosted Evals

When authenticated with Tessl, run hosted evals before updating benchmark numbers:

```bash
tessl project create --workspace martinfrancois java-optionals-skill
tessl eval run --variant with-context --variant without-context .
```

The headline benchmark should stay focused on implementation tasks that mirror the motivating
failures. Broad review and smoke scenarios can live in `evals-reference/` unless they're part of the
headline measurement.

The broader review scenarios in `evals-reference/` are useful while developing the skill, but many
are small snippets that a strong generic model can already solve without the skill. Keep them as
reference coverage unless they reveal a real implementation failure that belongs in the headline
benchmark.

## Benchmark Updates

When the hosted benchmark changes:

- record the run ID;
- record the content commit;
- update baseline and skill scores;
- update lift, raw score ratio, and missed-point reduction;
- keep the README wording clear about what the benchmark measures.

## Release Checklist

Release Please opens or updates a release pull request after changes land on `main`. Merging that
release pull request updates `CHANGELOG.md`, bumps `.tessl-plugin/plugin.json`, creates the GitHub
release, and then publishes the Tessl plugin from the release workflow.

Before merging a release pull request:

- run local checks;
- run hosted evals or confirm the current benchmark is still valid;
- test the skill against at least one Java Optional change outside this repository;
- confirm `README.md` stays user-focused;
- confirm contributor-only process details live here.
