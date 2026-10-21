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

The composition check from java-functional-style-skill, main suite with both skills as context,
`01a15e1e-be18-70e0-966e-0a4cba97a5e8`: six of seven at 100; `19` chose `findFirst` once and
scored 100 on its targeted rerun `01a15e29-f382-74b5-ba9d-dd315d3c479e`.
