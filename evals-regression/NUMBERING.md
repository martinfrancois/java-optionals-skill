# Scenario Numbering

Regression scenarios keep the number they had in `evals/` or `evals-reference/` when they move
here, so hosted run history and issue links stay readable. Gaps are intentional: the missing
numbers are scenarios that still live in the other two suites or were retired.

## Rebuild for the deepseek-v4.1-flash solver (2026-10-21)

Moved here with `evidence_type` `solved_regression` after the local screen in
`docs/agents/local-screening.md` scored both arms at 98 to 100 in every run (the table in
`evals-reference/NUMBERING.md` has the numbers): `04-frontmatter-port-feature` from `evals/`, and
`06`, `22`, `24`, `26`, `30`, `31`, `38`, `44`, `46`, `52` from `evals-reference/`. Their hosted
with-context run against the new skill text is still to come; keep them only if it scores 100.

`48` and `49` left: with natural prompts their baseline is 43 and 64, so they are lift material
(both reference after the hosted runs; `48` scored 100 unaided on Tessl). They had been placed here on hosted evidence from explicit
prompts under the September solver.

## Hosted run against 1.0.2 (2026-10-21)

With context only, run `01a15e1e-acc4-7308-869b-a0e060cb4183`: ten of the eleven scored 100.
`52-findany-equivalent-optional-matches` scored 0 there and again in the targeted rerun
`01a15e29-e8da-7519-b1d6-ba25773b8246`: the agent wrote no file, because the prompt said "return
the revised Java code only" without naming one, and Tessl's judge grades files. The prompt now
asks for `OptionalLookupTerminals.java`, and the rerun on that prompt
(`01a15e33-46b8-74ab-8c3a-34f47f2ebb31`) scored 100, so all eleven regression scenarios stand at
100 with the skill on the released text. `53` in reference had the same wording and the same fix;
its rerun with both arms (`01a15e33-5353-7278-9944-b0c5c13b045f`) scored 100 and 100.

The composition check from java-functional-style-skill on 2026-10-21
(`01a15e1e-be18-70e0-966e-0a4cba97a5e8`, and the rerun of `19`,
`01a15e29-f382-74b5-ba9d-dd315d3c479e`) activated neither skill on any scenario. The composed
runner passed no `--skill` until java-functional-style-skill#52, so those runs measured the
solver alone and are not evidence. The rerun with the fixed runner is
java-functional-style-skill#51.
## Moves from reference after the 1.0.2 remainder run (2026-11-01)

`07-absence-as-error` and `10-fake-optional-list` moved here from `evals-reference/` with
`evidence_type` `solved_regression`. Both scored 100 in both arms on two hosted runs: the cut-off
run `01a1604b-4e37-71f6-8737-adb2daf08687` and the remainder run
`01a19905-f63c-760a-8068-9fdd88056e3a`, the second on the prompt that names the file. `07` failed
unaided in the local screen (75), so its local and hosted baselines disagree; two clean hosted runs
outweigh the local screen, as `evals-reference/NUMBERING.md` sets for `53` and `60`.

`06-checked-io-boundary` scored 100 with context on its changed prompt, which now names the file,
in run `01a19906-1bca-746f-86b1-43cbf7148eb2`.

## Regression run on the trimmed presence rule, cut off (2026-11-02)

With context only, run `01a19ce4-14ac-775b-ac44-2d370fb9a71b`, on the skill text of PR #173. It
ended as failed when the organization's Tessl credits were blocked. Twelve of the thirteen
scenarios scored 100 with the skill activated; `38-implement-setup-options` has no finished cell
and is still owed on this text.

The composition check from java-functional-style-skill (commit `17ff2e6`) ran the main suite
with both skills in `01a19ce4-672f-770d-873d-0a9f030d351e` and was cut off the same way. `09`,
`37`, `51`, `55`, and `57` scored 100; `57` activated only java-optionals, the others both
skills. `45` has no finished cell and is still owed.

## Owed cells on the trimmed presence rule (2026-11-08)

The two cells the cut-off runs above left owed ran on `main` at `a809475`, whose skill text is the
PR #173 text:

- `38-implement-setup-options`, context only, `01a1ba83-c14d-7253-b74a-0a6201dc8047`: 100 with
  the skill activated. Every regression scenario now has a cell at 100 on this text.
- Composition `45-workflow-validation-cleanup`, from java-functional-style-skill `a44d37f`, both
  skills activated: 99 in `01a1ba83-da00-753d-b2a6-adddb3b50a35`, then 100 in the isolated rerun
  `01a1ba88-afce-707f-b985-953470dbd523`. The 99 lost one point on "Uses Optional as validation
  boundary": a generic helper returned the missing warning from an `isEmpty()` guard, then built
  the mismatch warning with `filter(...).map(...)` instead of one chain; it never called `get()`.
  The composition rule in `docs/agents/ownership-boundaries.md` reruns a single miss once in
  isolation and changes the wording only when the miss repeats; it didn't, so the skill text
  stays. With `09` gone to reference, `37`, `45`, `51`, `55`, and `57` each have a composition
  cell at 100.

## Regression on the prose constant-selection rule (2026-11-09)

All 13 regression scenarios ran with the skill only on the final text of #181, run
`01a1be6f-b43a-7277-a9b9-9fbcf5c7412c`, and scored 100 with the skill activated.
