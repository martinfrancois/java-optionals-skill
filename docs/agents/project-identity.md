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

- The GitHub repository started private. Don't make it public unless the user explicitly asks.
- The Tessl tile is published while the GitHub repository remains private.
- The goal is OSS readiness for the GitHub repository, not automatic public release. Tell the user
  when the repository looks ready to publish; don't make it public for them without an explicit
  request.
- Keep the project independent of company naming. Don't add company names to the repo name, package
  name, README, or public metadata unless the user asks.
- Don't mention private gists or secret references in public docs. Public origin links should point
  to `martin-francois/symphony-trello#96`.

## References

- [Public Metadata And OSS Readiness](public-metadata.md)
- [Workflow](workflow.md)
