# README Guidance

## Scope

Use this when editing `README.md`, examples, motivation wording, or user-facing docs.

## Reader Rules

- Write for users first. Tessl is the install path, not the main story.
- The README should quickly make a Java developer think: "This solves a real problem I have."
- Keep the README flow natural from top to bottom. People may read it in order, so avoid sections
  that feel like disconnected notes.
- Put Getting Started before the motivation section.
- Keep a table of contents.
- Keep contributor-only details in `CONTRIBUTING.md`, not in the README.
- Do not add random package-name blocks such as `martinfrancois/java-optionals` unless they are part
  of a real install command or are otherwise useful to the reader.
- Use simple words that non-native Java developers can understand.
- Avoid avoidable words such as "idiomatic", "rationale", "provenance", "fluent", "semantics",
  "nullable", "present/absent", "first-pass", and "DTO" in user-facing README text.
  Prefer "standard", "reason", "origin", "method chain", "business behavior", "values that may be
  null", "values that may or may not exist", "new code", and "data object".

## Motivation Rules

- Keep the opening hook concrete. Mention the real bad shapes early, such as `isPresent()` plus
  `get()`, `orElse(null)`, fallback work that runs too early, fake one-item lists, and clear streams
  rewritten as noisy loops.
- The core motivation is: AI agents already wrote Java `Optional` code, but often used bad patterns.
  When asked to clean it up, they sometimes replaced one bad pattern with another.
- Mention that the skill is based on real AI-written failures, not a made-up style preference.
- If changing the motivation, re-check the original issue body and all comments, plus the local
  source notes. The comments contained useful details that were easy to miss.
- Do not lose the issue-only cases that were added after the first audit: diagnostics selector
  Optionals and optional output side-effect handling.
- Do not imply the skill is only for refactoring. It helps agents write new Optional code well and
  clean up existing Optional code.
- Avoid vague phrases like "keep the same behavior" unless you name what must stay the same, such as
  outputs, errors, prompts, side effects, or when fallback work runs.
- Avoid phrases that make the examples sound like recommended transformations. They are bad outputs
  the skill is meant to prevent.

## Example Rules

- Use small, easy examples. Prefer an online-store domain when possible because most readers can
  understand it quickly.
- Keep the store examples intuitive: coupons, discounts, shipping codes, totals, customers, carts,
  and receipts are good. Avoid examples whose business story distracts from the Optional problem.
- Keep code samples as short as possible while still showing the failure.
- The README examples are not exact copies from the original issue. Phrase them accurately with
  "would have changed" or equivalent wording.
- In anti-examples, avoid generic `from` / `to` labels because they can imply the second half is the
  desired change.
- Prefer comments like:

  ```java
  // before the AI cleanup request
  // what an unassisted AI would have changed it to
  ```

- If mentioning a failure like "turning one Optional into a fake list", include a tiny code example
  so readers understand why it is bad.

## References

- [Skill Behavior](skill-behavior.md)
- [Public Metadata And OSS Readiness](public-metadata.md)
- [Maintaining Agent Docs](maintaining-agent-docs.md)
