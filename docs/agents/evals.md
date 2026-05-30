# Eval Guidance

## Scope

Use this when editing `evals/`, `evals-reference/`, skill evals, benchmark claims, or scoring rules.

## Rules

- Don't cheat. Don't leak the diagnosis or desired fix in eval prompts.
- Keep eval prompts neutral. Avoid clue words that tell the model the exact failure, such as
  "order-independent" or "preserving laziness", unless those words are truly part of the user task.
- The headline eval should mirror the real failure mode: implementation tasks where an agent writes
  or changes Java Optional code and may introduce Optional antipatterns.
- Include evals where the agent writes new Optional code, not only reviews or refactors snippets.
- Review-only or no-op evals must still require a concrete artifact, such as `review.md`, so empty
  answers can't pass by accident.
- Keep broad review or smoke scenarios in `evals-reference/` unless they're part of the headline
  benchmark.
- If the baseline is too high, first check whether the eval is too generic or too easy before
  changing the skill. The baseline should reveal the real failures from the issue.
- Be careful when tightening prompts or scoring. If a change mainly increases empty-output noise or
  brittle failures instead of measuring the Optional behavior better, revert or redesign it.
- A 2x raw score ratio is useful only when earned by honest, realistic eval design. Don't suppress
  legitimate coverage just to improve lift.
- Track raw score, percentage-point lift, raw score ratio, and missed-point reduction when updating
  benchmark claims.

## Checks

Run the shared validation commands in [Workflow](workflow.md). When editing eval criteria, also run
the criteria JSON check listed there.

## References

- [Workflow](workflow.md)
- [Skill Behavior](skill-behavior.md)
