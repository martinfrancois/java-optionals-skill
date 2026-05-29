# Source Notes

Use this file when maintaining the skill. Do not require ordinary skill users to read it.

## Origin

This skill was distilled from `martin-francois/symphony-trello` issue 96, "Propose java-optionals
agent skill", and all comments present when the skill was created.

The issue required the final skill to be self-contained. External links, the original repository
fixture, and the issue itself are research inputs, not operating instructions.

## Comment Integration

- 2026-05-19 13:07 UTC: Initial draft proved the issue could become a real skill folder with
  `SKILL.md`, `agents/openai.yaml`, and `references/optional-examples.md`. Checked-exception
  examples needed complete class/import context for copyable eval fixtures.
- 2026-05-19 23:42 UTC: Supporting files were made explicit because collapsible sections made them
  too easy to miss. This repository keeps them as real files.
- 2026-05-19 23:45 UTC: A secret gist provided a cleaner multi-file draft. The repository uses that
  draft as a source artifact, but not as a required runtime dependency.
- 2026-05-19 23:47 UTC: The draft was updated after checking pre-cleanup production code at the
  parent of `4aaa1a6e61572a932153578d3e48bb6a2923b0cf`. This skill explicitly says the guidance is
  based on observed production failures.
- 2026-05-19 23:48 UTC: Metadata and the default prompt were expanded to cover first-pass Java code
  writing, not only review and refactor work.
- 2026-05-19 23:51 UTC: The skill was strengthened so first-pass Optional code starts by choosing
  the Optional boundary before branches are written. Eval scoring now covers behavior preservation,
  laziness, public output, and avoiding null/list workarounds. Eval cases for repeated value reads,
  single-Optional-to-list/loop workarounds, and first-pass lazy cache creation were added.
- 2026-05-19 23:52 UTC: UI wording changed from "Safer Java Optional code" to "Java Optional best
  practices" to avoid overstating safety guarantees.
- 2026-05-19 23:53 UTC: Antipattern prevention was made explicit in metadata and opening text.
- 2026-05-19 23:55 UTC: Readability was made an explicit goal.
- 2026-05-19 23:56 UTC: The LinkedIn article was removed as insufficiently relevant.
- 2026-05-19 23:57 UTC: Source quality tiers were added. JDK docs are primary for API behavior;
  DZone is trusted project context; Pasdam, freeCodeCamp, and Trinity Logic are corroboration when
  consistent with JDK docs and observed failures; Medium articles and the GitHub gist are caution
  sources.
- 2026-05-20 00:02 UTC: The issue body was updated to say external articles are research only,
  useful content should be verified and extracted into the skill, and final operation must not
  require opening external links, repository fixtures, or the issue.
- 2026-05-29: A follow-up audit against the live issue and latest gist found that the gist still
  ended at the earlier eval set, while the issue body contained Case E for diagnostics selectors and
  output-path side effects. The repository now carries those lessons as first-class examples and
  eval scenarios.
- 2026-05-30: The hosted eval suite was revised because earlier prompts leaked the target diagnosis
  and generic smoke scenarios dominated the score. Prompts are now more neutral, review tasks write
  `review.md` to avoid empty-output artifacts, three adversarial review scenarios cover proposed bad
  cleanups, and smoke scenarios have lower weights than skill-specific classification cases.
- 2026-05-30: Added a first-pass Optional formatting eval where an agent writes `AssigneeFormatter`
  from scratch. This complements the lazy-cache writing eval by checking ordinary Optional code
  creation without `isPresent()`/`get()`, `orElse(null)`, or fake collection control flow.
- 2026-05-30: Tried to increase hosted eval lift without distorting the suite. Added a concrete
  selector priority pattern to `SKILL.md` after a usage-spec failure on first-pass selector writing,
  then added eight varied hard cases for priority fallback, fake single-Optional loops, eager
  fallback regressions, null error workarounds, value binding, Vavr dependency overreach,
  transform/filter writing, and repeated `get()` reviews. Hosted run
  `019e75ef-251c-713f-8562-013af9c3fef3` at commit `24542ab` scored baseline `773/888` and
  usage-spec `887/888`. This is not a 2x raw-score ratio because the baseline solves much of the
  broader Java suite, but it leaves only 1 missed usage-spec point and avoids cherry-picking.
- 2026-05-30: Re-read issue 96 and confirmed that the motivating failures happened during ordinary
  AI implementation work, not only review-only tasks. The hosted benchmark was refocused on
  implementation-regression scenarios that start from branchy AI-written code and ask for feature
  work. Broader smoke/review scenarios were preserved under `evals-reference/`. After tightening
  real-collection matcher guidance, hosted run `019e7611-55fd-717e-80bd-e9446d5ad34b` at commit
  `d267f22` scored baseline `276/616` and usage-spec `616/616`, a `2.23x` raw score ratio and full
  missed-point reduction on the focused suite.

## Source Treatment

- Primary: JDK Optional documentation for API facts.
- Trusted: DZone Optional antipattern guidance where it matches the accepted project context.
- Corroboration: Pasdam, freeCodeCamp, and Trinity Logic when consistent with JDK behavior and the
  observed failures.
- Caution: Medium posts and third-party gists. Use only individual points after independent
  checking.
- Removed: LinkedIn article from the draft discussion.

## Validation Fixture

The production fixture commit `4aaa1a6e61572a932153578d3e48bb6a2923b0cf` in
`martin-francois/symphony-trello` is a validation set, not training data. Use portable examples for
skill wording and use the fixture only to check whether the skill generalizes.
