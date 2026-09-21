# Ownership Boundaries

## Scope

Use this when changing runtime guidance, README wording, evals, or companion-package documentation
for Java Optionals. This page holds the only full list of who owns what; other pages link here.

## Rules

- `java-optionals` owns Optional behavior: absence handling, fallback behavior, Optional API choice,
  fallback laziness as Optional behavior, Java-version compatibility, primitive Optionals, checked
  IO, prompt, and parser boundaries, and present/empty/error contract preservation. It keeps its own
  lazy-fallback rule and its rule against hiding checked boundaries behind generic Optional helpers,
  because the published Optional evals measure them.
- `martinfrancois/java-functional-style` owns general Java lambda and functional-interface style:
  identity functions, no-op functional stages, helper extraction from block callbacks, comparator
  composition, method-reference pitfalls (receiver binding, overloads, boxing), supplier laziness as
  callback style, checked-exception boundaries inside callbacks, and callback side-effect
  boundaries.
- `martinfrancois/java-streams` owns stream and collector behavior.
- Each package works on its own. Don't make Optional guidance depend on the companion being
  installed, and don't remove Optional guidance because the companion also covers it.
- Don't add generic `Function.identity()`, no-op callback-stage, or broad callback-readability
  rules here to cover companion behavior. Optional examples may use concise lambdas or suppliers to
  show Optional behavior; they aren't the canonical source for general functional style.

## Composition Check

Adding the companion must not make this skill worse. The check runs this repository's evals,
unchanged, with both skills injected as context and requires 100% with-context for every scenario
in the run:

```bash
# from a checkout of java-functional-style-skill, next to this repository
scripts/run_composed_eval.sh ../java-optionals-skill main
```

The main suite is required whenever either package changes runtime text; run `reference` and
`regression` too when the change touches review wording or when budget allows. The companion
repository owns the runner and runs the check before its releases; this repository runs it when
its own runtime changes. Local validation alone doesn't satisfy this check.

## References

- [Skill Behavior](skill-behavior.md)
- [README Guidance](readme.md)
- [Eval Guidance](evals.md)
- [Workflow](workflow.md)
