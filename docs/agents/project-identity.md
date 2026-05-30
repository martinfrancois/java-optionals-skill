# Project Identity

## Scope

Use this when naming the repository, skill, package, workspace, or public source links.

## Rules

- Repository name: `java-optionals-skill`.
- Skill name: `java-optionals`.
- Tessl package name: `martinfrancois/java-optionals`.
- Tessl workspace: `martinfrancois`.
- If the Tessl project needs to be recreated, use:

  ```bash
  tessl project create --workspace martinfrancois java-optionals-skill
  ```

- The GitHub repository started private. Do not make it public unless the user explicitly asks.
- The goal is OSS readiness, not automatic public release. Tell the user when it looks ready to
  publish; do not publish it for them without an explicit request.
- Keep the project independent of company naming. Do not add company names to the repo name, package
  name, README, or public metadata unless the user asks.
- Do not mention private gists or secret references in public docs. Public origin links should point
  to `martin-francois/symphony-trello#96`.

## References

- [Public Metadata And OSS Readiness](public-metadata.md)
- [Workflow](workflow.md)
