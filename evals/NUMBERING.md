# Scenario Numbering

The main eval set keeps historical scenario numbers so hosted run comparisons and PR discussion
links stay understandable. Gaps are intentional when scenarios move to `evals-reference/` or
`evals-regression/`.

## Rebuild for the deepseek-v4.1-flash solver (2026-10-21)

The suite was rebuilt from the local screen in `docs/agents/local-screening.md` (DeepSeek V4.1
Flash, the model behind Tessl's default solver; a Claude Haiku judge; not hosted evidence). Of
the former main scenarios, `04` scored 100 unaided and moved to regression, `11` (now reference
`59`) and `50` fail unaided but their skill arm sits at 90 to 97, so they wait in reference.

The six scenarios here are the natural prompts whose baseline sits at least 30 points under 100
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

With the skill, locally, each scored 100 in every run on the final text (the runs are listed
below once the final screen completes). Hosted confirmation of the main suite with both arms is
recorded here when it exists.
