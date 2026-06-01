# Java Optional Replay And Eval Plan

This is the tracked plan for proving whether `java-optionals` helps on the real Symphony for Trello
Optional failures before turning them into Tessl evals.

## Goal

Build trustworthy evals from real historical failures.

Evidence chain:

1. A real historical Symphony prompt without the skill reproduces a bad Optional pattern.
2. The same prompt from the same commit with the skill avoids the bad pattern.
3. Behavior is preserved.
4. A reduced standalone eval reproduces the same without-skill vs with-skill difference.
5. Skill changes are driven by replay evidence, not by score-chasing.

## Hard Rules

- Do not mutate the main Symphony checkout.
- Use disposable worktrees.
- Start every replay from the exact historical starting commit.
- Run the same prompt with and without the skill.
- Do not strengthen historical prompts to make the skill look better.
- Cap every Codex execution at 30 minutes.
- Do not promote a scenario to an eval until full-repository replay proves it is useful.
- Do not tune evals for a prettier score.
- Behavior and compilation matter more than Optional style.

## Phase 1: Prepare Replay Workspace

- [x] Confirm current `java-optionals-skill` repo state.
- [x] Confirm Symphony for Trello repo path.
- [x] Create replay workspace under `/tmp/java-optionals-replay-20260531-165239`.
- [x] Create disposable worktrees for replay runs.
- [x] Confirm with-skill setup: global Tessl install from this PR branch.
- [x] Confirm 30-minute execution cap with `timeout 1800s`.

## Phase 2: Full-Repository Replay

For each scenario:

1. Check out the exact starting commit in a without-skill worktree.
2. Run the historical prompt without the skill.
3. Stop after 30 minutes if still running.
4. Capture diff, checks, bad Optional patterns, and behavior concerns.
5. Check out the exact same starting commit in a with-skill worktree.
6. Run the same historical prompt with `java-optionals`.
7. Stop after 30 minutes if still running.
8. Capture the same data.
9. Classify the scenario.
10. Write results back to [results.md](results.md).

### Scenario A: `.orElse(null)` Follow-Up On PR #89

- [x] Without-skill replay run.
- [x] With-skill replay run.
- [x] Results recorded.
- [x] Classification recorded.

Classification:

```text
reference only until narrowed
```

Notes:

```text
Without-skill reproduced internal `orElse(null)` cleanup risk. The with-skill run was broad and
still introduced fake one-Optional stream/list flow, so the full prompt is too noisy as a direct
eval source.
```

### Scenario B: Remaining Value Reads In PR #89

- [x] Without-skill replay run.
- [x] With-skill replay run.
- [x] Results recorded.
- [x] Classification recorded.
- [x] Skill improved until with-skill replay passes.

Classification:

```text
reduced into headline eval
```

Notes:

```text
Without-skill reproduced checked Optional helper overreach. Earlier with-skill runs replaced one
antipattern with another. Valid with-skill-v10 read the installed skill, avoided fake helpers and
iterables, passed full Maven verification after formatting, and became headline eval 11.
```

### Scenario C: Single Optional Converted To A Stream/List

- [x] Without-skill replay run.
- [x] With-skill replay run.
- [x] Results recorded.
- [x] Classification recorded.
- [x] Reduced-eval attempt recorded.

Classification:

```text
strong full-repo candidate, reduced eval not faithful yet
```

Notes:

```text
Without-skill reproduced checked Optional helper overreach. A later with-skill replay avoided the
helper and fake stream/list patterns with narrow checked-boundary branches. Two hosted runs of the
reduced scenario did not reproduce the helper/list failure in the baseline, so the reduced case is
reference material, not headline evidence.
```

### Scenario D: Stable Workflow Ports

- [x] Without-skill replay run.
- [x] With-skill replay run.
- [x] Results recorded.
- [x] Classification recorded.

Classification:

```text
reference only
```

Notes:

```text
No distinct Optional failure was found in changed production code in either run.
```

### Scenario E: Scoped Trello Handoff Tools

- [x] Without-skill replay run.
- [x] With-skill replay run.
- [x] Results recorded.
- [x] Classification recorded.

Classification:

```text
reference only / mine for smaller first-pass evals
```

Notes:

```text
The full prompt is broad and noisy. The with-skill run did not produce a focused Optional cleanup
oracle; keep it as reference material unless a smaller first-pass implementation case is extracted.
```

### Scenario F: Deterministic Pickup Transition

- [x] Without-skill replay run.
- [x] With-skill replay run.
- [x] Results recorded.
- [x] Classification recorded.

Classification:

```text
reference only / mine for smaller cleanup evals
```

Notes:

```text
The with-skill run changed the requested pickup flow but left unrelated pre-existing Optional
value-reopening patterns in touched files. It needs a narrower oracle before it becomes an eval.
```

## Phase 3: Interpret Full-Repo Results

- [x] Scenario classifications reviewed.
- [x] Scenarios needing skill changes identified.
- [x] Scenarios excluded from immediate evals documented with reasons.
- [x] Scenarios selected for reduction attempted or documented as not ready.

Classifications used:

- `strong eval candidate`: without-skill reproduces the bad pattern, with-skill avoids it, and
  behavior is preserved.
- `skill needs improvement first`: both runs reproduce the bad pattern, or with-skill avoids the
  pattern but breaks behavior.
- `not useful for eval reduction`: without-skill no longer reproduces the bad pattern, the scenario
  is too noisy, or the result depends on unrelated choices.
- `reference only`: historically important but too broad or hard to replay faithfully.

## Phase 4: Skill Improvement Loop

Only do this when a with-skill full-repository replay still produces a bad Optional pattern or
breaks behavior.

- [x] Identify the exact skill gap for Scenario B.
- [x] Update skill guidance narrowly.
- [x] Avoid answer keys or scenario-specific repository instructions.
- [x] Run skill validators.
- [x] Rerun Scenario B after first hardening.
- [x] Record failed before/after results.
- [x] Continue until Scenario B passes or a concrete blocker is documented.

Scenario B resolution:

```text
Scenario B with-skill-v10 was the first valid passing replay. Earlier with-skill-v8 and v9 were not
valid proof because the Codex sandbox could not read the installed skill. The valid run used
`--sandbox danger-full-access`, read `java-optionals`, avoided the fake helper/list moves, and
passed `./mvnw -q spotless:check verify` after `spotless:apply`.
```

## Phase 5: Reduce Proven Scenarios Into Evals

Only start this for scenarios classified as `strong eval candidate`.

For each selected scenario:

1. Extract the smallest code fixture that still contains the real failure shape.
2. Preserve the real behavior constraints.
3. Prefer a simple domain when it makes the scenario easier to understand.
4. Run the reduced prompt without the skill.
5. Run the reduced prompt with the skill.
6. Cap each run at 30 minutes.
7. Compare the reduced result with the full-repository result.
8. Keep reducing or adjust the fixture until the reduced eval reproduces the same difference.
9. Discard the reduced eval if it stops matching full-repository evidence.

Progress:

- [x] Scenario C reduced and checked; reduced hosted baseline did not reproduce the full-repo helper
  failure, so it was kept in `evals-reference/`.
- [x] Scenario B reduced into `evals/11-checked-boundary-selection-cleanup`; hosted baseline
  reproduced the targeted Optional-quality failures while preserving behavior.
- [x] Scenario A already has focused workpad/upsert coverage in existing headline/reference evals;
  no new reduction was needed from the broad full-repo replay.
- [x] Scenario E/F were reviewed after with-skill runs and left as reference only; no smaller
  optional-specific oracle was selected.

## Phase 6: Add Tessl Evals

For each reduced scenario that reproduces the full-repo difference:

- [x] Add reference scenario files in the current Tessl format for Scenario C.
- [x] Add headline scenario files in the current Tessl format for Scenario B.
- [x] Include `capability.txt`.
- [x] Include `task.md`.
- [x] Include `criteria.json`.
- [x] Classify invocation style.
- [x] Include compile/artifact checks where applicable.
- [x] Include behavior checks.
- [x] Keep Optional style below behavior/compilation in scoring priority.
- [x] Avoid runtime answer-key leakage.
- [x] Keep Scenario C out of the headline suite because the reduced baseline did not reproduce the
  historical helper/list failure.
- [x] Update docs to report natural, explicit, headline, and reference results honestly.

## Phase 7: Validate And Report

- [x] Run local validators after final edits.
- [x] Start hosted Tessl eval run for updated headline suite.
- [x] Record quality and lift from hosted run.
- [x] Record which scenarios were included, excluded, or kept as reference.
- [x] Explain whether lift changed because evals now better reflect historical failures.
- [x] Do not claim broader skill quality than the evidence supports.

## Current Status

```text
The full plan is implemented. Scenario B now has a valid passing with-skill replay and a faithful
headline reduction. Scenario C remains reference-only because the reduced baseline did not reproduce
the full-repo helper/list failure. Scenario A is preserved as reference coverage because the focused
headline suite now keeps only direct evidence for the plugin summary. Scenario E/F are documented as
reference-only because the broad prompts did not yield smaller useful Optional oracles. Latest
hosted focused headline run is `019e811b-e9da-71fb-adf6-74fb3265a68d`: baseline `146/300`, with
context `298/300`, `2.04x`.
```
