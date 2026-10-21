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
