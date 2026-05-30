# Workflow

## Scope

Use this for day-to-day work in this repository: auth checks, validation, commits, and pushes.

## Rules

- If a Tessl or GitHub command fails because auth, login, workspace, or permission state appears
  missing, re-check after the user says they changed it. Do not keep assuming the old state.
- When the user asks for autonomous work, carry it through implementation, validation, commit, and
  push unless they explicitly ask to stop earlier.
- Before committing changes to the skill, README, evals, package metadata, agent docs, or this file,
  run:

  ```bash
  python3 /root/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/java-optionals
  tessl plugin lint .
  tessl plugin publish --dry-run --skip-evals .
  ```

- When editing eval criteria, also run:

  ```bash
  find evals -name criteria.json -print0 | xargs -0 -n1 jq empty
  ```

- Commit and push finished changes unless the user explicitly asks not to.

## References

- [Project Identity](project-identity.md)
- [Eval Guidance](evals.md)
- [Public Metadata And OSS Readiness](public-metadata.md)
