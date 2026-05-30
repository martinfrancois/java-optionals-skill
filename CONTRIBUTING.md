# Contributing

Thanks for helping improve the Java Optional Skill.

This project helps AI coding agents write and clean up Java `Optional` code without replacing one
bad pattern with another. You don't need maintainer access or a Tessl workspace to make most useful
contributions.

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

## Local Setup

Clone the repository, make your change on a branch, and run the local checks below before opening a
pull request. There are no project dependencies to install for the Python validation scripts.

The Tessl CLI is only needed for `tessl plugin lint` and publish dry-runs. If you don't have Tessl
set up locally, still run the Python checks and mention that Tessl checks were not run in your pull
request.

## Local Checks

Run these before committing skill, eval, README, package, script, or CI changes:

```bash
python3 scripts/validate_skill.py skills/java-optionals
python3 scripts/validate_eval_criteria.py evals evals-reference
tessl plugin lint .
```

If you have Tessl access, you can also run the publish dry-run:

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

Hosted evals are useful when a change affects the skill behavior, benchmark scenarios, or README
score claims. They require Tessl authentication and a linked Tessl project.

If you have your own Tessl workspace, link your checkout to your own project and run:

```bash
tessl eval run --variant with-context --variant without-context .
```

If you don't have a Tessl workspace, that's fine. Open the pull request with the local check results,
and a maintainer can run the hosted evals before release.

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

Releases are handled by maintainers. Release Please opens or updates a release pull request after
changes land on `main`. Merging that release pull request updates `CHANGELOG.md`, bumps
`.tessl-plugin/plugin.json`, creates the GitHub release, and then publishes the Tessl plugin from the
release workflow.

Before merging a release pull request:

- run local checks;
- run hosted evals or confirm the current benchmark is still valid;
- test the skill against at least one Java Optional change outside this repository;
- confirm `README.md` stays user-focused;
- confirm contributor-only process details live here.

## Dependency Updates

Renovate keeps GitHub Actions, commitlint, and pinned action digests current. Major updates need
manual approval from the dependency dashboard.
