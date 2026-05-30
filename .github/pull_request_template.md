## Summary

Describe the change in 2-5 bullet points.

- Problem:
- Why it matters:
- What changed:
- What did not change:

## Change Type

Choose all that apply.

- [ ] Skill behavior
- [ ] Evals or scoring
- [ ] Documentation
- [ ] CI, release, or dependency automation
- [ ] Repository metadata or contribution process
- [ ] Other maintenance

## Linked Issue

- Fixes #
- Related #

## User-Visible Behavior

Describe what a user, contributor, or maintainer can observe after this PR. If there is no
user-visible change, write `None`.

## Bug Fix Details

For bug fixes or regressions, explain why the issue happened and what now prevents it from coming
back. For other changes, write `N/A`.

- Root cause:
- Test, eval, or guardrail added:
- If no test or eval was added, why not:

## Validation

List the commands, manual checks, or hosted checks you ran. Include relevant failures that were fixed
during the PR.

Checks most contributors can run:

- [ ] `python3 scripts/validate_skill.py skills/java-optionals`
- [ ] `python3 scripts/validate_eval_criteria.py evals evals-reference`
- [ ] `tessl plugin lint .`
- [ ] `markdownlint`, if Markdown changed
- [ ] Manual rendered-doc or example review, if docs or examples changed

Tessl-authenticated checks:

- [ ] `bash scripts/check_publish_dry_run.sh .`
- [ ] `tessl skill review --threshold 85 skills/java-optionals/SKILL.md`, if skill text or references changed
- [ ] `tessl eval run --variant with-context --variant without-context .`, if skill behavior,
      evals, or benchmark claims changed

`bash scripts/check_publish_dry_run.sh .`, `tessl skill review`, and hosted Tessl evals require
Tessl authentication. Hosted evals also require a linked Tessl project. If you can't run one of
them, leave it unchecked and explain why in the details.

Details:

```text

```

## Human Verification

Describe what you tried manually and what result you saw. If the change cannot be tried manually,
explain why.

```text

```

## Review Checklist

- [ ] Docs updated, or N/A
- [ ] Evals updated, or N/A
- [ ] PR title or squash title uses Conventional Commits
- [ ] Redaction checked: no Tessl tokens, GitHub tokens, package manager tokens, private repository
      links, private eval artifacts, private registry/workspace links, local host paths, or
      proprietary Java source

## AI Assistance (if used)

<!--
AI-assisted PRs are welcome. Mark this when an AI tool materially helped write, design, or edit the
change so reviewers know what to look for.
-->

- [ ] AI-assisted PR
- [ ] I confirm I understand and reviewed the change

<details>
<summary>AI prompts / session logs (optional)</summary>

```text

```

</details>
