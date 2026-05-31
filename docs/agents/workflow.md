# Workflow

## Scope

Use this for day-to-day work in this repository: auth checks, validation, commits, and pushes.

## Rules

- If a Tessl or GitHub command fails because auth, login, workspace, or permission state appears
  missing, re-check after the user says they changed it. Don't keep assuming the old state.
- When the maintainer explicitly asks for autonomous pull request work, carry it through
  implementation, validation, commit, push, and PR creation unless they ask to stop earlier.
- Before committing changes to the skill, README, evals, package metadata, scripts, CI, agent docs,
  or this file, run:

  ```bash
  python3 scripts/validate_skill.py skills/java-optionals
  python3 scripts/validate_eval_criteria.py evals evals-reference
  python3 -m py_compile scripts/validate_skill.py scripts/validate_eval_criteria.py
  bash -n scripts/check_publish_dry_run.sh
  tessl plugin lint .
  bash scripts/check_publish_dry_run.sh .
  tessl plugin publish --dry-run --bump patch .
  tessl plugin publish --dry-run .
  ```

- After a version has been published, the dry-run may fail only because that exact version already
  exists. For docs-only changes that don't need a new plugin release, record that as expected and don't
  bump the version. For skill, eval, or package changes that should be published, bump the
  version before publishing again.

- CI mirrors the portable validation checks. When `TESSL_TOKEN` is configured, it also runs a fast
  skipped-eval publish dry-run and a full eval-ingesting publish dry-run. The optional skill review
  workflow runs `tessl skill review --threshold 90` when `TESSL_TOKEN` is configured.
- Use bumped publish dry-runs for PR convenience when the current manifest version is already
  published. Use exact-version dry-runs in release publishing before the real publish command.
- Keep the review threshold below 100 unless the maintainer explicitly wants a hard 100 gate. Don't
  remove useful Java guidance only to improve the review score.
- Pull request titles and commits must use Conventional Commits. Release Please uses them to update
  `CHANGELOG.md`, `.tessl-plugin/plugin.json`, and GitHub releases. Tessl publishing happens only in
  `.github/workflows/publish-tessl.yml` on `release: published` or manual dispatch.
- Renovate manages GitHub Actions, action digests, commitlint packages, and the pinned Tessl CLI
  version in workflows. Keep `minimumReleaseAge` at 7 days with `internalChecksFilter: "strict"` so
  Renovate waits before creating branches or PRs for updates that haven't passed the age gate. Keep
  custom managers only for dependencies Renovate can't detect natively: commitlint packages installed
  inside workflow shell commands, and the Tessl CLI version passed to `tesslio/setup-tessl`. Don't
  add Maven, Docker, or vendored Tessl dependency rules unless those files exist here.

- For maintainer-requested automation tasks where the user has asked for a pull request, commit and
  push finished changes. Otherwise, don't push without explicit instruction.

## References

- [Project Identity](project-identity.md)
- [Eval Guidance](evals.md)
- [Public Metadata And OSS Readiness](public-metadata.md)
