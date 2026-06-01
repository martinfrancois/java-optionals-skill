# Eval Guidance

## Scope

Use this when editing `evals/`, `evals-reference/`, skill evals, benchmark claims, or scoring rules.

## Rules

- Don't cheat. Don't leak the diagnosis or desired fix in eval prompts.
- Keep eval prompts neutral. Avoid clue words that tell the model the exact failure, such as
  "order-independent" or "preserving laziness", unless those words are truly part of the user task.
- The headline eval should mirror the real failure mode: tasks where an agent writes or changes Java
  Optional code and may introduce Optional antipatterns.
- Keep a documented mix of invocation styles:
  - Natural activation scenarios don't mention `$java-optionals`, "use the skill", or similar
    command-style phrasing.
  - Explicit invocation scenarios may say `Use $java-optionals`.
  - Report natural, explicit, headline-combined, and reference/full results separately when hosted
    data is available.
- Include evals where the agent writes new Optional code, not only reviews or refactors snippets.
- Review-only or no-op evals must still require a concrete artifact, such as `review.md`, so empty
  answers can't pass by accident.
- Keep broad review or smoke scenarios in `evals-reference/` unless they're part of the headline
  benchmark.
- Every scenario directory must contain `task.md`, `criteria.json`, and `capability.txt`.
- Every `criteria.json` must classify `metadata.invocation` and `metadata.task_type`.
- Every headline criterion must classify `category` as `safety`, `optional_quality`, or
  `maintainability`.
- Headline implementation scenarios need compile/artifact checks and behavior checks as safety
  gates, but the headline score should mainly measure Optional-specific quality.
- Treat compile and behavior checks as safety gates. They should stop broken answers from looking
  good, but this skill's public benchmark should be weighted toward the `optional_quality` subtotal
  because the skill is not primarily trying to improve compilation.
- Runtime skill references must not contain eval inventories, expected answers, score rubrics,
  hosted run IDs, or fixed score claims. Keep those in maintainer docs such as
  [eval-case-inventory.md](eval-case-inventory.md) or [source-notes.md](source-notes.md).
- Java scenarios should state a baseline when API compatibility matters, and criteria should catch
  accidental use of APIs newer than that baseline.
- If the baseline is too high, first check whether the eval is too generic or too easy before
  changing the skill. The baseline should reveal the real failures from the issue.
- Be careful when tightening prompts or scoring. If a change mainly increases empty-output noise or
  brittle failures instead of measuring the Optional behavior better, revert or redesign it.
- A 2x raw score ratio is useful only when earned by honest, realistic eval design. Don't suppress
  legitimate coverage just to improve lift.
- Track raw score, percentage-point lift, raw score ratio, missed-point reduction, and the
  `optional_quality` subtotal when updating benchmark claims.
- Don't hide scenarios merely because the baseline solves them. Move them to `evals-reference/`
  only when they're better as broader regression coverage, and document why.
- For transcript-derived cases, use the historical replay protocol before adding headline evals.
  The reduced eval should reproduce the same without-skill vs with-skill difference seen in the
  full repository. If the with-skill replay still fails, record it as a regression target instead of
  promoting it as a passing eval.

## Checks

Run the shared validation commands in [Workflow](workflow.md). When editing eval criteria, also run
the criteria JSON check listed there.

## References

- [Workflow](workflow.md)
- [Skill Behavior](skill-behavior.md)
- [Historical Replay](replay/README.md)
