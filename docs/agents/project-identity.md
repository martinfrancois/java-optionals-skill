# Project Identity

## Scope

Use this when naming the repository, skill, package, workspace, or public source links.

## Rules

- Repository name: `java-optionals-skill`.
- Skill name: `java-optionals`.
- Tessl package name: `martinfrancois/java-optionals`.
- Tessl workspace: `martinfrancois`.
- The GitHub repository is public. Keep public docs free of private paths, local transcript paths,
  unpublished workspace details, and secret references.
- The Tessl plugin manifest is public with `"private": false`; keep it that way unless the
  maintainer asks to return to private package metadata.
- If `tessl project repair` cannot relink this checkout and the Tessl project needs to be
  recreated, use the pinned CLI project command:

  ```bash
  tessl project create --workspace martinfrancois java-optionals-skill
  ```

  Do this only for project identity recovery. It is not part of normal plugin publishing, release,
  or eval execution.

- Keep the project independent of company naming. Don't add company names to the repo name, package
  name, README, or public metadata unless the user asks.
- Don't mention private gists or secret references in public docs. Public origin links should point
  to `martin-francois/symphony-trello#96`.

## References

- [Public Metadata And OSS Readiness](public-metadata.md)
- [Workflow](workflow.md)
