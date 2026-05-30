# AGENTS.md

Project-specific instructions for future agents working in this repository.

## Project Identity

- Repository name: `java-optionals-skill`.
- Skill name: `java-optionals`.
- Tessl package name: `martinfrancois/java-optionals`.
- Tessl workspace: `martinfrancois`.
- The GitHub repository started private. Do not make it public unless the user explicitly asks.
- The goal is OSS readiness, not automatic public release. Tell the user when it looks ready to
  publish; do not publish it for them without an explicit request.
- If the Tessl project needs to be recreated, use:

  ```bash
  tessl project create --workspace martinfrancois java-optionals-skill
  ```

- Keep the project independent of company naming. Do not add company names to the repo name,
  package name, README, or public metadata unless the user asks.
- Do not mention private gists or secret references in public docs. Public origin links should point
  to `martin-francois/symphony-trello#96`.

## Durable Corrections

When the user corrects wording, naming, scope, eval design, public metadata, or project policy, make
that correction durable here. Do not treat corrections as one-off chat feedback. Update this file so
future agents start from the corrected preference.

Before finalizing a README, skill, eval, or metadata change, skim this file and check that the change
still follows these rules.

## README Rules

- Write for users first. Tessl is the install path, not the main story.
- The README should quickly make a Java developer think: "This solves a real problem I have."
- Keep the opening hook concrete. Mention the real bad shapes early, such as `isPresent()` plus
  `get()`, `orElse(null)`, fallback work that runs too early, fake one-item lists, and clear streams
  rewritten as noisy loops.
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
- Keep the README flow natural from top to bottom. People may read it in order, so avoid sections
  that feel like disconnected notes.

## Motivation Wording

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

## Skill Triggering

- The skill should not require users to explicitly type `$java-optionals` every time.
- Metadata should let agents auto-select it for Java tasks involving `Optional`, `isPresent()`,
  `orElse(null)`, `optional.stream()`, `findFirst()` / `findAny()`, missing values, values that may
  be `null`, fallback/default values, and code where a value may or may not exist.
- The README may say: "agents that support skill auto-selection, such as Codex and Claude Code".
- Before naming platforms that support auto-selection, verify against official docs and link those
  docs when possible.
- Do not over-explain install-path differences in the Getting Started flow.

## Operations

- If a Tessl or GitHub command fails because auth, login, workspace, or permission state appears
  missing, re-check after the user says they changed it. Do not keep assuming the old state.
- When the user asks for autonomous work, carry it through implementation, validation, commit, and
  push unless they explicitly ask to stop earlier.

## Eval Rules

- Do not cheat. Do not leak the diagnosis or desired fix in eval prompts.
- Keep eval prompts neutral. Avoid clue words that tell the model the exact failure, such as
  "order-independent" or "preserving laziness", unless those words are truly part of the user task.
- The headline eval should mirror the real failure mode: implementation tasks where an agent writes
  or changes Java Optional code and may introduce Optional antipatterns.
- Include evals where the agent writes new Optional code, not only reviews or refactors snippets.
- Review-only or no-op evals must still require a concrete artifact, such as `review.md`, so empty
  answers cannot pass by accident.
- Keep broad review or smoke scenarios in `evals-reference/` unless they are part of the headline
  benchmark.
- If the baseline is too high, first check whether the eval is too generic or too easy before
  changing the skill. The baseline should reveal the real failures from the issue.
- Be careful when tightening prompts or scoring. If a change mainly increases empty-output noise or
  brittle failures instead of measuring the Optional behavior better, revert or redesign it.
- A 2x raw score ratio is useful only when earned by honest, realistic eval design. Do not suppress
  legitimate coverage just to improve lift.
- Track raw score, percentage-point lift, raw score ratio, and missed-point reduction when updating
  benchmark claims.

## Public Metadata

- GitHub description should be short, clickable, and user-benefit focused.
- Current preferred shape: "Help AI coding agents use Java Optional well in new code and cleanup,
  without replacing one bad pattern with another."
- Use the maximum useful number of relevant discoverability topics when the repo becomes public.
- If asked about topics, report how many GitHub repositories exist for each topic when you can.
- Before calling the repo OSS-ready, check for a license, no private/secret references, a
  user-focused README, contributor docs, passing lint, and benchmark claims that match the current
  evals.

## Validation

Run these before committing changes to the skill, README, evals, package metadata, or this file:

```bash
python3 /root/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/java-optionals
tessl plugin lint .
tessl plugin publish --dry-run --skip-evals .
```

When editing eval criteria:

```bash
find evals -name criteria.json -print0 | xargs -0 -n1 jq empty
```

Commit and push finished changes unless the user explicitly asks not to.
