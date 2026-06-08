# Public Metadata And OSS Readiness

## Scope

Use this when editing GitHub metadata, release readiness docs, package metadata, public docs, or repo
topics.

## Rules

- GitHub description should be short, clickable, and user-benefit focused.
- Current preferred wording: "Help AI coding agents use Java Optional well in new code, review, and
  cleanup without replacing one antipattern with another."
- Use the maximum useful number of relevant discoverability topics for the public repository.
- If asked about topics, report how many GitHub repositories exist for each topic when you can.
- Before calling the repo OSS-ready, check for a license, no private/secret references, a
  user-focused README, contributor docs, passing lint, and benchmark claims that match the current
  evals.
- Tessl packaging currently uses `.tessl-plugin/plugin.json`. Keep docs, scripts, workflows, and
  release config aligned with plugin terminology unless official docs and CLI behavior change.
- Do not add `tile.json` unless current Tessl docs and CLI behavior require it.
- The workflow-pinned Tessl CLI version accepts the current plugin format with
  `.tessl-plugin/plugin.json`.
  `tessl plugin lint .`, `tessl plugin publish --dry-run --skip-evals .`, and
  `tessl plugin publish --dry-run --bump patch .` are the authority for package validity here.
  `tessl plugin pack` must include `skills/java-optionals/SKILL.md` and the referenced files under
  `skills/java-optionals/references/`. Do not add a `skills` field or migrate to `tile.json` unless
  those pinned CLI checks or current official docs prove the active skill is not included,
  discoverable, or publishable.

## References

- [Project Identity](project-identity.md)
- [README Guidance](readme.md)
- [Eval Guidance](evals.md)
