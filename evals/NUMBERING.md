# Scenario Numbering

The main eval set keeps historical scenario numbers so hosted run comparisons and PR discussion
links stay understandable. Gaps are intentional when scenarios move to `evals-reference/` or
`evals-regression/`.

## Rebuild for the deepseek-v4.1-flash solver (2026-10-21)

The suite was rebuilt from the local screen in `docs/agents/local-screening.md` (DeepSeek V4.1
Flash, the model behind Tessl's default solver; a Claude Haiku judge; not hosted evidence). Of
the former main scenarios, `04` scored 100 unaided and moved to regression, `11` (now reference
`59`) and `50` fail unaided but their skill arm sits at 90 to 97, so they wait in reference.

The scenarios here are the natural prompts whose baseline sits at least 30 points under 100
and whose skill arm reached 100 locally. `13`, `48`, `51`, `55`, and `57` were reweighted to the
main policy (15 safety, 80 Optional-quality, 5 maintainability) when they moved; `13` also grew
from 12 to 100 points and gained an artifact and a focus item.

| Scenario | Runs | Without skill (1.0.1 criteria) | What the solver does unaided |
| --- | --- | --- | --- |
| `10-first-pass-retry-backoff` | 2 | 32 (30 to 34) | null checks and `isPresent()` plus `get()` for the header and the parse |
| `13-output-path-side-effect` | 2 | 42 | keeps `isPresent()` and `orElseThrow()` around the write |
| `48-workpad-feature-cleanup` | 2 | 43 (42 to 44) | `isPresent()` then `get()` for the update-or-create decision |
| `51-presence-selects-enum-value` | 2 | 42 (40 to 44) | keeps the `isPresent()` ternary, sometimes inside a new helper |
| `55-side-effecting-ifpresentorelse-lookup` | 2 | 64 (63 to 65) | `isPresent()` then `orElseThrow()` for the lookup branch |
| `57-catalog-validation-bound-once` | 2 | 64 (59 to 68) | `isPresent()` paired with `get()` twice in the validator |

### After the reweighting, on the final skill text (2026-10-21)

Baseline two runs each against the main-policy checklists (six for `13`, which is bimodal), skill
arm three runs each (`57` six, after its "binds once" item was reworded to say it judges one
method, not whether two methods may each call the catalog):

| Scenario | Without skill | With skill |
| --- | --- | --- |
| `10-first-pass-retry-backoff` | 41 (31 to 50) | 99 (97 to 100): the local judge docks a point for a hand-written digit scan |
| `13-output-path-side-effect` | 57 (35 in three runs, 100 in three) | 100 |
| `48-workpad-feature-cleanup` | 23 (19 to 27) | 100 |
| `51-presence-selects-enum-value` | 37 (36 to 38) | 100 |
| `55-side-effecting-ifpresentorelse-lookup` | 40 (39 to 40) | 100 |
| `57-catalog-validation-bound-once` | 46 (42 to 50) | 100 |

Hosted confirmation of the main suite with both arms is recorded here when it exists.

## Hosted run on the PR #142 text (2026-10-21)

Both arms, run `01a15bf4-3181-75bf-b471-984b8b2cd5e3`, default solver, the six scenarios placed
by the local screen:

| Scenario | Baseline | With skill |
| --- | --- | --- |
| `10-first-pass-retry-backoff` | 19 | 100 |
| `13-output-path-side-effect` | 100 | 100 |
| `48-workpad-feature-cleanup` | 100 | 100 |
| `51-presence-selects-enum-value` | 35 | 100 |
| `55-side-effecting-ifpresentorelse-lookup` | 35 | 100 |
| `57-catalog-validation-bound-once` | 43 | 100 |

`13` and `48` solved unaided on this run (`13` is bimodal locally; `48` had scored 19 to 44 in
four local runs) and moved to `evals-reference/`, since the main floor is a 30-point gap on the
hosted run. The main suite is `10`, `51`, `55`, `57`: 132 without the skill against 400 with it.
`19`, `35`, and `37` (local baselines 58, 60, 69; skill arm 100) were reweighted to the main policy
and run hosted as the next candidates in `01a15bfa-b287-71d3-b44d-bc199631c480`:

| Scenario | Baseline | With skill |
| --- | --- | --- |
| `19-first-pass-redacted-option` | 65 | 100 |
| `35-implement-diagnostics-command` | 52 | 100 |
| `37-implement-frontmatter-port` | 60 | 100 |

All three clear the 30-point floor and joined the suite. The main suite is `10`, `19`, `35`,
`37`, `51`, `55`, `57`: 309 without the skill against 700 with it on these two hosted runs, about
2.3x. The publish-time run of the whole suite is recorded here when it exists.
