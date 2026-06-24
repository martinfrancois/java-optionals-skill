# Eval Guidance

## Scope

Use this when editing `evals/`, `evals-reference/`, `evals-regression/`, skill evals,
benchmark claims, or scoring rules.

## Rules

- Don't cheat. Don't leak the diagnosis or desired fix in eval prompts.
- Run quality review first, and if it is below 100%, stop and fix all quality issues before any new
  hosted eval rerun. Then execute targeted evals for every changed scenario, and only progressively
  broaden suites after targeted runs are clean. Preserve the daily budget by stopping at each stage
  unless failures require another targeted rerun; only then proceed to broader hosted checks. If a
  broad run shows any with-context below 100%, stop that run and return to targeted reruns for failed
  scenarios only.
- Keep natural activation prompts neutral. Avoid clue words that tell the model the exact failure,
  such as "order-independent" or "preserving laziness", unless those words are truly part of the
  user task. Explicit invocation prompts may name `$java-optionals`, but they should not leak the
  diagnosis or desired fix beyond invoking the skill.
- The Java Optional skill is broadly about Optional correctness, readability, fallback timing,
  boundary handling, stream interop, primitive Optional usage, and avoiding cleanup changes that
  replace one antipattern with another.
- The main eval set is evidence-weighted: it should cover core skill capabilities and give more
  weight to scenario families where hosted runs show the largest improvement with the skill versus
  without it. Read the main score as "where this skill measurably helps most," not as an evenly
  sampled survey of every Optional API.
- The main eval should mirror the real failure mode: tasks where an agent writes or changes Java
  Optional code and may introduce Optional antipatterns.
- The main suite should include at least one scenario for each core capability area that the skill
  claims to improve when a useful with-vs-without delta exists, higher weights for scenario families
  with the largest missed-point reduction, natural and explicit invocation scenarios reported
  separately, and reference scenarios kept separate unless promoted and normalized.
- When choosing or weighting main scenarios, prefer hosted eval evidence: baseline score,
  with-context score, raw score lift, missed-point reduction, and whether failures match real
  observed Optional mistakes.
- Do not promote a reference scenario into main only for topical balance if the baseline already
  solves it and the skill adds little measurable value. Keep low-delta diagnostic cases in
  `evals-reference/`; move repeatedly solved cases to `evals-regression/` only when hosted history
  shows both with-context and without-context are consistently 100%.
- Keep a documented mix of invocation styles:
  - Natural activation scenarios don't mention `$java-optionals`, "use the skill", or similar
    command-style phrasing.
  - Explicit invocation scenarios may say `Use $java-optionals`.
  - Report natural, explicit, main eval combined, reference, and regression results separately when
    hosted data is available.
- Include evals where the agent writes new Optional code, not only reviews or refactors snippets.
- Review-only or no-op evals must still require a concrete artifact, such as `review.md`, so empty
  answers can't pass by accident.
- Skill-context-dependent evals require information that only comes from the skill package or agent
  instructions, such as exact wording, commands, procedures, checklists, headers, or bundled
  reference text. Keep them in `evals-regression/` once with-context is 100%, regardless of the
  without-context score. Do not count them in the main or reference lift score, do not describe them
  as natural activation or independent Java Optional reasoning, and do not call weighted checklist
  items hard gates.
- Keep three eval buckets:
  - `evals/` is the main eval set used for public lift reporting.
  - `evals-reference/` is for candidate, diagnostic, and broad coverage scenarios that may still
    help tune or promote future main evals.
  - `evals-regression/` is for scenarios that hosted history shows are consistently solved by both
    with-context and without-context, plus skill-context-dependent checks that are only fair as
    with-context regression coverage. These protect against regressions but should not be part of
    normal lift discovery runs.
- Every scenario directory must contain `task.md`, `criteria.json`, and `capability.txt`.
- Every `criteria.json` must classify `metadata.invocation` and `metadata.task_type`.
- Use `metadata.evidence_type` when scenario placement needs to be explicit:
  - `ordinary_lift`: an ordinary main or reference scenario where both variants are fair to compare.
    This value is invalid in `evals-regression/`.
  - `solved_regression`: a regression scenario moved because hosted evidence shows both variants
    repeatedly score 100%.
  - `skill_context_dependent`: a regression scenario that requires skill-package or agent-instruction
    context, so without-context comparison is not fair.
- Every main eval criterion must classify `category` as `safety`, `optional_quality`, or
  `maintainability`.
- Main eval implementation scenarios need compile/artifact checks and behavior checks as safety
  checks, but the main score should mainly measure Optional-specific quality.
- Treat compile and behavior checks as safety-category checks. They make broken answers visible in
  the score, but this skill's public benchmark should be weighted toward the `optional_quality`
  subtotal because the skill is not primarily trying to improve compilation.
- For main eval scenarios, use roughly `15` safety points, `80` Optional-quality points, and `5`
  maintainability points per 100-point scenario unless a scenario has a documented reason to differ.
- `evals/11-checked-boundary-selection-cleanup` is intentionally weighted as a 60-point main eval
  case because checked-boundary scoring is noisier and should not dominate the combined main eval
  score. Its category ratio still follows the main eval policy: roughly 15% safety, 80%
  Optional-quality, and 5% maintainability.
- `evals-reference/45-workflow-validation-cleanup` remains reference coverage. It is intentionally
  not part of the focused main eval set because the active main eval set should stay concentrated on
  the clearest Optional-quality signal.
- Runtime skill references must not contain eval inventories, expected answers, score rubrics,
  hosted run IDs, or fixed score claims.
- Every Java scenario, including temporary candidate scenarios, must state the Java version to
  assume, such as `Assume Java 17.`. Criteria should catch accidental use of APIs newer than that
  baseline.
- If the baseline is too high, first check whether the eval is too generic or too easy before
  changing the skill. The baseline should reveal the real failures from the issue.
- Be careful when tightening prompts or scoring. If a change mainly increases empty-output noise or
  brittle failures instead of measuring the Optional behavior better, revert or redesign it.
- A 2x raw score ratio is useful only when earned by honest, realistic eval design. Don't suppress
  legitimate coverage just to improve lift.
- Track raw score, percentage-point lift, raw score ratio, missed-point reduction, and the
  `optional_quality` subtotal when updating benchmark claims.
- If with-context is below 100%, keep the scenario in its current suite. Fix the skill or eval in
  place and run that scenario targeted until it is clean before running broader suites. Do not move
  failing with-context scenarios to hide them.
- Promote or demote scenarios based on purpose and evidence:
  - `with-context < 100`: targeted fix/rerun in place.
  - `with-context = 100` and `without-context < 100`: useful lift evidence; keep in main or
    reference depending on coverage and weighting.
  - `with-context = 100` and `without-context = 100` repeatedly: candidate for
    `evals-regression/`.
- A new scenario should not move to main unless its percentage-point delta is at least 30 percentage
  points and it improves capability coverage. Treat 30 pp as maintainer policy for future promotion
  or demotion decisions, not as a current hosted benchmark result. Old hosted deltas are historical
  evidence only; do not use them for release-readiness claims, public score/lift claims, or current
  benchmark claims until they are rerun against the current active suite membership, denominator,
  commit/ref, natural/explicit split, and pinned CLI behavior.
- Don't hide scenarios merely because the baseline solves them. Move them to `evals-regression/`
  only when they're consistently solved by both variants and are better as safety-net coverage than
  lift or diagnostic evidence.
- For transcript-derived cases, compare the reduced scenario against available replay evidence, PR
  notes, or git history before adding main evals. The reduced eval should reproduce the same
  without-skill vs with-skill difference seen in the full repository. If the with-skill replay still
  fails, record it as a regression target instead of promoting it as a passing eval.
- Historical eval inventories, replay plans, hosted-run notes, and legacy eval formats are not kept
  as active documentation. Keep current policy in these docs and use git history for old answer
  keys, replay logs, and one-off run details.
- Keep hosted eval usage minimal while preserving confidence:
  - Use `scripts/run_eval_suite.sh` so variants match suite purpose and runs use the plugin context.
  - Main and reference scenarios run with both variants.
  - Regression scenarios run with context only by default. Run regression without-context only when
    intentionally checking whether a scenario should move back to reference.
  - For skill or eval changes, first run only the affected scenario directories.
  - If any affected with-context result is below 100%, keep rerunning only those targeted scenarios
    after fixes until they are clean.
  - Then run `evals/` for the main score.
  - Run relevant `evals-reference/` scenarios when deciding promotion or checking nearby behavior.
  - Run `evals-regression/` as a final safety check before release or after broad changes, not on
    every tuning loop.
  - A pure move between `evals/`, `evals-reference/`, and `evals-regression/` does not need a hosted
    rerun when `task.md`, scoring criteria, and `capability.txt` are unchanged except for
    suite-placement metadata or numbering notes.

Current active suite structure:

- `evals/`: 4 scenarios, 360 checklist points, 3 natural and 1 explicit.
- `evals-reference/`: 46 scenarios, 2470 checklist points, broad candidate and diagnostic coverage.
- `evals-regression/`: 2 scenarios, 200 checklist points, with-context safety coverage.

## Checks

Run the shared validation commands in [Workflow](workflow.md). When editing eval criteria, also run
the criteria JSON check listed there.

## References

- [Workflow](workflow.md)
- [Skill Behavior](skill-behavior.md)
