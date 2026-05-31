# Java Optional Historical Replay

This directory records the full-repository replay work used to decide whether real Symphony for
Trello Optional failures are ready to become Tessl evals.

The replay evidence chain is:

1. Start from the exact historical Symphony commit before the user prompt.
2. Run the historical prompt without `java-optionals`.
3. Reset to the same commit.
4. Run the same prompt with `java-optionals`.
5. Compare bad Optional patterns, behavior risk, and checks.
6. Only reduce a case into a Tessl eval when the full-repository replay shows the same
   without-skill vs with-skill difference we want the eval to measure.

## Hard Rules

- Use disposable worktrees, not the main Symphony checkout.
- Do not strengthen historical prompts to help the skill.
- Cap each Codex execution at 30 minutes.
- Do not promote a scenario only because it improves a score.
- Behavior, compilation, laziness, exception messages, prompts, and branch order matter more than
  Optional style.

## Files

- [protocol.md](protocol.md): repeatable replay procedure.
- [results.md](results.md): current replay results and classifications.
- [eval-candidates.md](eval-candidates.md): reduced eval ideas that are not yet active evals.
