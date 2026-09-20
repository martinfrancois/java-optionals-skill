# Ownership Boundaries

## Scope

Use this when changing runtime guidance, README wording, evals, or companion-package documentation
for Java Optionals.

## Rules

- `java-optionals` owns Optional behavior: absence handling, fallback behavior, Optional API choice,
  fallback laziness as Optional behavior, Java-version compatibility, primitive Optionals, checked
  IO and prompt boundaries, parser boundaries, and present/empty/error contract preservation.
- `java-functional-style` owns general Java lambda and functional-interface style: method
  references, identity functions, no-op functional stages, callback readability, helper extraction,
  supplier/callback style, and callback side-effect boundaries.
- `java-streams` owns stream and collector behavior: terminal operation choice, collector choice,
  duplicate-key and null behavior, encounter order, primitive streams, parallel streams, gatherers,
  and stream-specific behavior preservation.
- Do not add generic `Function.identity()`, no-op callback-stage, or broad callback-readability
  rules to `java-optionals` just to cover companion-package behavior.
- It is fine for Optional examples to use concise lambdas or suppliers when needed to demonstrate
  Optional behavior. Do not present those examples as the canonical source for general functional
  style.
- The expected high-quality setup for Optional cleanup involving non-trivial callbacks or generic
  functional-interface style is both `java-optionals` and `java-functional-style`.
- Each package must work on its own. Do not make Optional guidance depend on the companion being
  installed, and do not remove Optional guidance because the companion also covers it. The
  lazy-fallback rule stays here because the published Optional evals measure it.

## Composition Check

Before a release of either package changes what the pair does together, prove on the existing
Optional evals, unchanged:

```text
java-optionals alone (published) <= java-optionals + java-functional-style (with-context)
```

Run the Optional `evals/` suite (and `evals-reference/` plus `evals-regression/` when budget allows)
with both skills as context and require 100% with-context for every retained scenario. The
companion repository ships the runner for this check (`scripts/run_composed_eval.sh` in
`java-functional-style-skill`). Local validation alone does not satisfy this check.

## References

- [Skill Behavior](skill-behavior.md)
- [README Guidance](readme.md)
- [Eval Guidance](evals.md)
