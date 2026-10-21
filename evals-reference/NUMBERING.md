# Scenario Numbering

Reference scenarios keep historical numbers from earlier suites. Gaps are intentional when a case
was removed, renamed, promoted to main eval coverage, moved between main eval and reference
coverage, or moved to `evals-regression/` after repeated both-variant 100% results.

Numbers `51` to `58` were added on 2026-10-20 from the open eval issues (one scenario per issue;
the issue link is in each `criteria-meta.json`; `51` to `56` take their code from draft PR #75).
`59` is the former main scenario `11-checked-boundary-selection-cleanup`, renumbered because
`11-lazy-cache-writing` already held that number here.

## Rebuild for the deepseek-v4.1-flash solver (2026-10-21)

Every scenario went through the local screen in `docs/agents/local-screening.md` (DeepSeek V4.1
Flash as the solver, a Claude Haiku judge against each `criteria.json`; percentages, mean over the
runs, range in brackets). Not hosted evidence. Prompts were made natural first: 48 scenarios had
opened with "Use `$java-optionals` to ...", and none of their sources shows the maintainer naming
the skill, so only `54` (issue #70, where he did) stays explicit.

The placement rule: a baseline of 98 to 100 in every run with the skill arm at 98 or more is
regression; a baseline at least 30 points under 100 with the skill arm at 100 is a main
candidate; everything else is reference. The skill arm column names the skill text it was
measured against: `skill-v0` is the 1.0.1 text, `skill-v1` adds the rules from issues #67 to #77,
`skill-v2` the side-effect and helper-parameter rules.

| Scenario | Baseline runs | Without skill | With skill (runs, text) | Suite |
| --- | --- | --- | --- | --- |
| `01-display-name` | 2 | 88 | 100 (2, skill-v0) | reference |
| `02-lazy-upsert` | 2 | 98 (95 to 100) | 100 (2, skill-v0) | reference |
| `03-real-collection-stream` | 2 | 77 (75 to 79) | 100 (2, skill-v0) | reference |
| `04-frontmatter-port-feature` | 2 | 100 | 100 (2, skill-v0) | regression |
| `04-keep-findfirst` | 2 | 80 (73 to 86) | 100 (2, skill-v0) | reference |
| `05-use-findany` | 2 | 97 (94 to 100) | 100 (2, skill-v0) | reference |
| `06-checked-io-boundary` | 2 | 100 | 100 (2, skill-v0) | regression |
| `07-absence-as-error` | 2 | 75 (70 to 80) | 100 (2, skill-v0) | reference |
| `08-nullable-interop` | 2 | 73 (58 to 88) | 100 (2, skill-v1) | reference |
| `09-repeated-reads` | 2 | 96 (92 to 100) | 100 (2, skill-v0) | reference |
| `10-fake-optional-list` | 2 | 98 (95 to 100) | 100 (2, skill-v0) | reference |
| `10-first-pass-retry-backoff` | 2 | 32 (30 to 34) | 100 (99 to 100) (2, skill-v0) | evals |
| `11-lazy-cache-writing` | 2 | 95 (90 to 100) | 100 (2, skill-v0) | reference |
| `12-selector-optional` | 2 | 93 | 100 (2, skill-v0) | reference |
| `13-output-path-side-effect` | 2 | 42 | 100 (2, skill-v0) | reference |
| `14-review-null-workaround` | 2 | 94 (91 to 97) | 98 (97 to 100) (2, skill-v0) | reference |
| `15-review-loop-overcorrection` | 2 | 72 (43 to 100) | 98 (97 to 100) (2, skill-v0) | reference |
| `16-review-checked-helper` | 2 | 81 (70 to 92) | 99 (98 to 100) (2, skill-v0) | reference |
| `17-first-pass-optional-formatting` | 2 | 96 (91 to 100) | 97 (2, skill-v0) | reference |
| `18-first-pass-selector-writing` | 2 | 89 (88 to 90) | 100 (2, skill-v1) | reference |
| `19-first-pass-redacted-option` | 2 | 58 (55 to 60) | 100 (2, skill-v0) | evals |
| `20-review-legacy-null-boundary` | 2 | 75 | 100 (2, skill-v1) | reference |
| `21-review-optional-dto-overreach` | 2 | 78 (75 to 80) | 100 (2, skill-v1) | reference |
| `22-review-findany-order-regression` | 2 | 100 | 100 (2, skill-v1) | regression |
| `23-first-pass-output-routing` | 2 | 64 (28 to 100) | 100 (2, skill-v0) | reference |
| `24-first-pass-priority-fallback` | 2 | 100 | 100 (2, skill-v0) | regression |
| `25-review-single-optional-stream-loop` | 2 | 94 (92 to 95) | 100 (2, skill-v0) | reference |
| `26-review-eager-fallback-regression` | 2 | 100 | 100 (2, skill-v0) | regression |
| `27-review-null-error-workaround` | 2 | 92 (90 to 95) | 100 (2, skill-v0) | reference |
| `28-first-pass-card-move-plan` | 2 | 78 (75 to 80) | 100 (2, skill-v0) | reference |
| `30-first-pass-clean-label` | 2 | 100 | 100 (2, skill-v0) | regression |
| `31-review-repeated-get-cleanup` | 2 | 99 (98 to 100) | 100 (2, skill-v0) | regression |
| `32-implement-workpad-upsert` | 2 | 79 (58 to 100) | 100 (2, skill-v0) | reference |
| `33-implement-command-sanitizer` | 2 | 54 (40 to 69) | 100 (2, skill-v1) | reference |
| `34-implement-workspace-resolution` | 2 | 94 (91 to 98) | 99 (98 to 100) (2, skill-v0) | reference |
| `35-implement-diagnostics-command` | 2 | 60 (60 to 61) | 100 (2, skill-v0) | evals |
| `36-implement-card-move-if-configured` | 2 | 85 (70 to 100) | 100 (2, skill-v0) | reference |
| `37-implement-frontmatter-port` | 2 | 69 | 100 (2, skill-v0) | evals |
| `38-implement-setup-options` | 2 | 100 (99 to 100) | 100 (2, skill-v0) | regression |
| `39-diagnostics-feature-cleanup` | 2 | 56 (54 to 58) | 99 (98 to 100) (2, skill-v0) | reference |
| `40-card-move-feature` | 2 | 80 | 100 (2, skill-v0) | reference |
| `41-setup-defaults-feature` | 2 | 88 (82 to 94) | 98 (97 to 100) (2, skill-v0) | reference |
| `42-primitive-optional-side-effect` | 2 | 94 (92 to 97) | 100 (2, skill-v0) | reference |
| `43-tri-state-optional-boolean` | 2 | 86 (83 to 89) | 100 (2, skill-v0) | reference |
| `44-predicate-only-optional-check` | 2 | 100 | 100 (2, skill-v0) | regression |
| `45-workflow-validation-cleanup` | 2 | 62 (56 to 67) | 100 (2, skill-v1) | reference |
| `46-normalized-product-feed` | 2 | 100 | 100 (2, skill-v0) | regression |
| `47-checked-boundary-fake-optional-list-cleanup` | 2 | 94 (94 to 95) | 100 (2, skill-v0) | reference |
| `48-workpad-feature-cleanup` | 2 | 43 (42 to 44) | 100 (2, skill-v0) | reference |
| `49-workspace-prompt-feature` | 2 | 64 (60 to 67) | 96 (94 to 97) (2, skill-v1) | reference |
| `50-command-sanitizer-feature` | 2 | 53 (44 to 62) | 96 (95 to 98) (2, skill-v2) | reference |
| `51-presence-selects-enum-value` | 2 | 42 (40 to 44) | 100 (99 to 100) (2, skill-v2) | evals |
| `52-findany-equivalent-optional-matches` | 2 | 100 | 100 (2, skill-v1) | regression |
| `53-domain-selection-lazy-fallback` | 2 | 99 (98 to 100) | 98 (96 to 100) (2, skill-v0) | reference |
| `54-optional-upsert-side-effect-boundary` | 2 | 100 | 100 (2, skill-v1) | reference |
| `55-side-effecting-ifpresentorelse-lookup` | 2 | 64 (63 to 65) | 100 (2, skill-v0) | evals |
| `56-optional-helper-trigger-lifecycle-refactor` | 2 | 61 (50 to 72) | 96 (95 to 96) (2, skill-v2) | reference |
| `57-catalog-validation-bound-once` | 2 | 64 (59 to 68) | 100 (1, skill-v2) | evals |
| `58-scoped-fallback-strategy-selection` | 2 | 34 (32 to 35) | 90 (87 to 92) (2, skill-v2) | reference |
| `59-checked-boundary-selection-cleanup` | 2 | 54 (50 to 57) | 90 (88 to 93) (2, skill-v2) | reference |

Placement followed the table: `13`, `48`, `51`, `55`, and `57` joined `10` in `evals/`, then the
hosted runs of 2026-10-21 sent `13` and `48` back here (baseline 100 on Tessl) and promoted `19`,
`35`, and `37` (see `evals/NUMBERING.md`); `04`,
`06`, `22`, `24`, `26`, `30`, `31`, `38`, `44`, `46`, and `52` moved to `evals-regression/`;
`48` and `49` came back from regression because the natural prompt fails unaided; the former main
scenarios `50` and `59` moved here because their skill arm sits at 90 to 97 on the current text.
`53` stays here although both arms are near 100 because its skill arm dipped to 96 in one run.
`54` stays here as the explicit-invocation coverage. `58` is the ScopedValue case from issue #77, rewritten
after the code review to start from an existing `ScopedValue` as the issue describes; unaided it
scores 97 to 100 (the presence check is the only miss). Earlier drafts of the task bound the
value with `Carrier.get(Supplier)`, which Java 23 removed, and penalized the solver for
correcting it to `call`; the task now uses `call` itself. It stays reference until a hosted run
shows where it lands.

`33` and `45` fail unaided (54 and 62) but their skill arm was below 100 in one local run each
(45 and 94), so they wait here under the with-context rule rather than joining main.
