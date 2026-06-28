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
- Before opening a PR that changes Optional runtime guidance or evals as part of this split, prove:

```text
current java-optionals behavior <= slimmed java-optionals + java-functional-style behavior
```

- The comparison must use the existing Optional evals unchanged until the composed setup is equal or
  better at criterion level. Local validation alone is not enough for that quality gate.

## References

- [Skill Behavior](skill-behavior.md)
- [README Guidance](readme.md)
- [Eval Guidance](evals.md)
