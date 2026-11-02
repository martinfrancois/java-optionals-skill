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

All three clear the 30-point floor and joined the suite. After the code review, `51` lost a
sentence that hinted at the fix and screened at 37 to 41 unaided in four runs of six (88 and 100
in the other two), and its skill arm stayed at 100 in every run; `57` scored 100 in four runs of
four with the skill after its binding item was reworded to judge one method. The main suite is `10`, `19`, `35`,
`37`, `51`, `55`, `57`: 309 without the skill against 700 with it on these two hosted runs, about
2.3x. The whole suite then ran on the text after the code review (commit `44ca38a`) in
`01a15c11-3ac0-7586-a566-3cff1dd3955d` (2026-10-21, both arms):

| Scenario | Baseline | With skill |
| --- | --- | --- |
| `10-first-pass-retry-backoff` | 34 | 100 |
| `19-first-pass-redacted-option` | 45 | 100 |
| `35-implement-diagnostics-command` | 44 | 100 |
| `37-implement-frontmatter-port` | 54 | 100 |
| `51-presence-selects-enum-value` | 33 | 98 |
| `55-side-effecting-ifpresentorelse-lookup` | 35 | 100 |
| `57-catalog-validation-bound-once` | 35 | 100 |

280 without the skill against 698 with it. `51` lost two points for routing the audit branch
through `ifPresent`, which the skill text had allowed next to a plain branch; the rule now keeps
a present branch that also writes something as a plain branch. `51` then ran targeted twice,
once on the text before that rule (`01a15c17-6b8e-779d-b95e-7821ec3a34d9`) and once on the final
text (`01a15c17-f69d-778f-b366-a392b597cc21`): 33 without the skill and 100 with it both times.
`58` ran as a further candidate (`01a15c16-e557-7343-a72a-49d6240fe607`) and scored 100 in
both arms, so it stays in reference.

Two wording commits to the skill followed the run above, so the whole suite ran once more on the
final text (commit `83ea794` of the skill) in `01a15c21-7bb2-73fe-813e-d177ea0f2a88`:

| Scenario | Baseline | With skill |
| --- | --- | --- |
| `10-first-pass-retry-backoff` | 24 | 100 |
| `19-first-pass-redacted-option` | 80 | 100 |
| `35-implement-diagnostics-command` | 58 | 100 |
| `37-implement-frontmatter-port` | 59 | 100 |
| `51-presence-selects-enum-value` | 29 | 100 |
| `55-side-effecting-ifpresentorelse-lookup` | 35 | 100 |
| `57-catalog-validation-bound-once` | 53 | 100 |

338 without the skill against 700 with it, about 2.1x; every main scenario at 100 with the
skill on the text that ships. `19` swings between 45 and 80 unaided across runs, which the
baseline columns of the three runs above show.

## Scenarios whose answer is a skill example (2026-11-02)

`10`, `19`, and `35` moved to `evals-reference/` under the rule in `docs/agents/evals.md`: a
scenario whose starting code, or the behavior its task specifies, and its expected answer both
appear as a worked example in the runtime references is not main evidence, identifiers renamed or
not.

- `10-first-pass-retry-backoff`: the references' `flatMap` example has the same nullable response,
  the same `Retry-After` header, `parseRetryAfter`, and the better shape
  `Optional.ofNullable(response).flatMap(...).flatMap(this::parseRetryAfter).orElseGet(...)`, which
  is the scenario's 60-point item.
- `19-first-pass-redacted-option`: the task has no starting code, but it specifies the
  `CommandRedactor` lookup (a `Set` of options matched on `equals` or `startsWith(option + "=")`),
  and the example's better shape ends in `findAny()`.
- `35-implement-diagnostics-command`: the selector and output-sink examples rewritten as an
  implementation task; both better shapes are in the references.

The four that stay, `37`, `51`, `55`, `57`, overlap the references only through Optional API names
or a one-line prose description of a general rule; each `criteria-meta.json` says which in
`runtime_reference_overlap_rationale`. In hosted run `01a19cac-5099-75d5-adec-f704024dd23c` they
scored 183 without the skill against 400 with it, about 2.19x. Main now has no `findAny`, retry
header, or selector scenario; moving those skill examples to another domain would let the three
scenarios come back.

## Promotion of the six reference candidates (2026-11-02)

The reference run on the 1.0.2 text recommended main for `01`, `05`, `09`, `12`, `45`, and `59`
from one run each (see `evals-reference/NUMBERING.md`). `12` was not run: it is the selector
example in the runtime references, starting code and better shape included. For the runs below,
`01`, `05`, `09`, and `45` were reweighted to the main policy (15 safety, 80 Optional quality, 5
maintainability, 100 points); `01`, `05`, and `09` gained an artifact item and a focus item.
`59` kept its documented 60-point checklist, whose ratio already matches.

Local screen on the main-policy checklists (DeepSeek V4.1 Flash, Haiku judge, not hosted evidence):

| Scenario | Without skill | With skill |
| --- | --- | --- |
| `01-display-name` | 100 (2 runs) | 100 (2) |
| `05-use-findany` | 62 (12 to 100, 6 runs: 12, 15, 45, and three 100s) | 100 (2) |
| `09-repeated-reads` | 99 (93 to 100, 6) | 94 (92 to 95, 2), then 100 (2) after the reword below |
| `45-workflow-validation-cleanup` | 51 (47 to 55, 2) | 100 (2) |
| `59-checked-boundary-selection-cleanup` | 54 (53 to 55, 2) | 76 (70 to 90, 4) |

`09` lost points with the skill only on "Binds or maps once", whose old wording ("Uses map plus a
helper") let the judge demand a named helper for a correct `filter(...).map(...).orElse(card)`
chain; it now says the helper is optional. The local judge docked `59` for an `isEmpty()` guard
whose empty branch prompts and throws `IOException`, a shape its checklist awards full credit,
so `59` went to the hosted run unchanged.

Hosted run of the twelve-scenario suite with both arms, `01a19cac-5099-75d5-adec-f704024dd23c`,
on the 1.0.2 skill text; every with-skill cell had the skill activated:

| Scenario | Baseline | With skill |
| --- | --- | --- |
| `01-display-name` | 100 | 100 |
| `05-use-findany` | 15 | 98 |
| `09-repeated-reads` | 35 | 100 |
| `10-first-pass-retry-backoff` | 19 | 100 |
| `19-first-pass-redacted-option` | 80 | 100 |
| `35-implement-diagnostics-command` | 44 | 100 |
| `37-implement-frontmatter-port` | 55 | 100 |
| `45-workflow-validation-cleanup` | 55 | 100 |
| `51-presence-selects-enum-value` | 40 | 100 |
| `55-side-effecting-ifpresentorelse-lookup` | 35 | 100 |
| `57-catalog-validation-bound-once` | 53 | 100 |
| `59-checked-boundary-selection-cleanup` | 80 | 100 |

`09` and `45` joined main. `01` solved unaided and `59` missed the 30-point floor by ten points,
so both stay in `evals-reference/`. `05` lost two points with the skill on its new focus item for
moving the match condition into a private helper; the item was reworded to allow that, and the
targeted rerun `01a19cb7-c943-7411-813a-b961529c7126` scored 18 without the skill and 100 with
it. Review then found that `05` is the references' `CommandRedactor` example with renamed
identifiers: a `Set` stream filtered on `arg.equals(x) || arg.startsWith(x + "=")` ending in
`findFirst()`, whose better shape uses `findAny()`, the item worth 50 of its 100 points. Under the
rule in `docs/agents/evals.md` it stays in reference too.

Capability coverage, which the promotion rule asks for besides the 30-point gap: `45`'s
capability text is the same as `37`'s (and `35`'s, now in reference), Optional fallback logic in
an implementation task, and `09`'s bind-once cleanup overlaps the bind-once item of `57`. Neither
adds a new capability area; martinfrancois's go-ahead to promote these candidates is the reason
they moved. `05`'s capability matched `19`'s.

The main suite is `09`, `37`, `45`, `51`, `55`, `57`: 273 without the skill against 600 with it
in `01a19cac-5099-75d5-adec-f704024dd23c`, about 2.20x.

## Hosted run after the presence-read rule was stated once (2026-11-02)

The skill text changed after the 1.0.3 release: the rule against reading a value again after a
presence check is now stated once in the workflow, and the step 8 scan points to Hard Stops
instead of linking `hard-stops.md` a third time. Both arms, run
`01a19cda-1b44-71b3-ba4e-50c2b77e0001`; every with-skill cell had the skill activated:

| Scenario | Baseline | With skill |
| --- | --- | --- |
| `09-repeated-reads` | 100 | 100 |
| `37-implement-frontmatter-port` | 100 | 100 |
| `45-workflow-validation-cleanup` | 35 | 100 |
| `51-presence-selects-enum-value` | 38 | 100 |
| `55-side-effecting-ifpresentorelse-lookup` | 35 | 100 |
| `57-catalog-validation-bound-once` | 45 | 100 |

353 without the skill against 600 with it, about 1.70x. `09` scored 35 and `37` 55 unaided in
`01a19cac-5099-75d5-adec-f704024dd23c`, so both swing between runs; neither moved on one run.
