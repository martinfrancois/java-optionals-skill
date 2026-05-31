# Skill Behavior

## Scope

Use this when editing `skills/java-optionals/SKILL.md`, skill metadata, install guidance, or
auto-selection wording.

## Rules

- The skill shouldn't require users to explicitly type `$java-optionals` every time.
- Metadata should let agents auto-select it for Java tasks involving `Optional`, `isPresent()`,
  `orElse(null)`, `optional.stream()`, `findFirst()` / `findAny()`, missing values, values that may
  be `null`, fallback/default values, and code where a value may or may not exist.
- Skill guidance must start by detecting the project Java baseline before selecting Optional,
  primitive Optional, stream, collector, record, or collection APIs.
- Cover the full Optional family: `Optional<T>`, `OptionalInt`, `OptionalLong`, `OptionalDouble`,
  Optional-producing stream terminals, primitive stream terminals, and Optional-producing
  collectors.
- Keep `findAny()` guidance defensive. It is only right when all matches are equivalent and no
  ordering or priority contract depends on the first match.
- Boundary exceptions should stay narrow: checked IO, prompts, legacy null APIs, external APIs,
  genuine absence-as-error, and predicate-only presence checks.
- The README may say: "agents that support skill auto-selection, such as Codex and Claude Code".
- Before naming platforms that support auto-selection, verify against official docs and link those
  docs when possible.
- Don't over-explain install-path differences in the Getting Started flow.

## References

- [README Guidance](readme.md)
- [Eval Guidance](evals.md)
