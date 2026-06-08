# Regression Evals

This directory is for scenarios that are consistently solved by both the with-context and
without-context variants in hosted runs, plus skill-context-dependent scenarios that are only fair as
with-context regression checks.

Keep these scenarios out of the main lift score and out of normal reference-candidate runs. Run
them as a final safety check before release, after broad skill changes, or when the changed area is
directly related to one of these scenarios.

Run regression evals with context only by default:

```bash
scripts/run_eval_suite.sh regression
```

Do not run regression `without-context` during normal maintenance. Without-context regression runs
are only useful when deliberately checking whether a scenario should move back to
`evals-reference/`.

With-context must be 100% for every regression scenario. Do not move a scenario here just because it
currently fails with context. If with-context is below 100%, keep the scenario in its current suite,
fix the skill or eval in place, and run that scenario targeted until it is clean before moving on to
broader eval runs.

Skill-context-dependent scenarios also live here. They require exact skill-provided text, commands,
procedures, checklists, headers, or bundled reference text. Use their with-context results as
regression coverage and do not count their without-context scores as fair lift evidence, regardless
of how the without-context variant happens to score.

Mark skill-context-dependent scenarios with:

```json
"metadata": {
  "evidence_type": "skill_context_dependent"
}
```

Mark solved regression scenarios with:

```json
"metadata": {
  "evidence_type": "solved_regression"
}
```

Every regression scenario must declare either `solved_regression` or `skill_context_dependent`.
