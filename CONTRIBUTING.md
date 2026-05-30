# Contributing

Thanks for helping improve the Java Optional Skill.

This project helps AI coding agents write and clean up Java `Optional` code without replacing one
bad pattern with another. You don't need maintainer access or a Tessl workspace to make most useful
contributions.

Keep changes focused on the observed failure modes: weak Optional boundaries, null-style control
flow, fake single-Optional collections, eager fallback work, unclear checked-IO handling,
`findFirst()` / `findAny()` mistakes, and overcorrected collection streams.

## Community Standards

Please follow the [Code of Conduct](CODE_OF_CONDUCT.md) in issues, pull requests, discussions, and
reviews.

AI-assisted contributions are welcome. If AI materially helped with a change, follow the
[AI Contribution Policy](AI_CONTRIBUTION_POLICY.md) and disclose that in the pull request body.

For suspected vulnerabilities, don't open a public issue. Follow the private reporting path in the
[Security Policy](SECURITY.md).

## Repository Layout

```text
.
├── .tessl-plugin/plugin.json
├── .github/ISSUE_TEMPLATE/
├── .github/pull_request_template.md
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
├── AI_CONTRIBUTION_POLICY.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

- `.github/ISSUE_TEMPLATE/` and `.github/pull_request_template.md` guide public issues and pull
  requests.
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
- `AI_CONTRIBUTION_POLICY.md`, `CODE_OF_CONDUCT.md`, and `SECURITY.md` set expectations for AI
  assistance, project conduct, and private vulnerability reporting.

## Local Setup

Clone the repository, make your change on a branch, and run the local checks below before opening a
pull request. There are no project dependencies to install for the Python validation scripts.

The Tessl CLI is needed for Tessl linting, skill review, publish dry-runs, and hosted evals. If you
don't have Tessl set up locally, still run the Python checks and mention that Tessl checks were not
run in your pull request.

## Local Checks

Run these before committing skill, eval, README, package, script, or CI changes:

```bash
python3 scripts/validate_skill.py skills/java-optionals
python3 scripts/validate_eval_criteria.py evals evals-reference
tessl plugin lint .
```

If you change the skill text or reference files, also run:

```bash
tessl skill review --threshold 85 skills/java-optionals/SKILL.md
```

If you have Tessl access, you can also run the publish dry-run:

```bash
bash scripts/check_publish_dry_run.sh .
```

That dry-run may fail because the current version already exists in the registry. That's expected
after a version has already been published; any other failure needs investigation.

`tessl skill review`, `bash scripts/check_publish_dry_run.sh .`, and hosted evals require Tessl
authentication. Hosted evals also require a linked Tessl project. If you don't have access, include
the local checks you did run and say which Tessl checks need maintainer help.

## Commit Messages

Pull request titles and commits must use Conventional Commits. CI checks both the pull request title
and every commit in the pull request.

Use this shape:

```text
type(optional-scope): short description
```

Keep the description short, lowercase, and written as an action or result. Don't end it with a
period.

Common types in this repository:

- `feat`: user-facing skill behavior, new guidance, or new benchmark coverage.
- `fix`: correct wrong guidance, broken metadata, validation, CI, or release behavior.
- `docs`: README, contributing guide, source notes, examples, or contributor docs.
- `test`: eval scenarios, eval criteria, or validation coverage.
- `ci`: GitHub Actions, Renovate, Release Please, or publishing automation.
- `chore`: repository maintenance that doesn't change user-facing behavior.
- `refactor`: restructure docs, scripts, or skill text without changing behavior.

Scopes are optional. Use one when it makes the change easier to scan:

```text
feat(skill): add selector fallback guidance
test(evals): cover eager fallback regression
docs(readme): clarify why the skill exists
ci(renovate): wait seven days before update PRs
fix(release): publish Tessl releases with evals
```

Avoid vague or non-conventional messages:

```text
update stuff
fixes
README changes
WIP
```

Release Please uses Conventional Commits after changes land on `main`:

- `feat` normally creates a minor release.
- `fix` normally creates a patch release.
- `feat!`, `fix!`, or a `BREAKING CHANGE:` footer creates a major release.
- `docs`, `ci`, `chore`, `refactor`, and `test` usually don't create a release by themselves unless
  they include a breaking-change marker.

For breaking changes, use either form:

```text
feat!: change skill activation contract
```

or:

```text
feat: change skill activation contract

BREAKING CHANGE: agents must now load the skill through the new package name.
```

If your branch has several small commits, each commit still needs a valid message. It's fine to keep
history simple and use one clear commit for a focused pull request.

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
