# Scenario Numbering

Reference scenarios keep historical numbers from earlier suites. Gaps are intentional when a case
was removed, renamed, promoted to main eval coverage, moved between main eval and reference
coverage, or moved to `evals-regression/` after repeated both-variant 100% results.

Numbers `51` through `56` were added during the July 2026 open-issue sweep. They cover reference
scenarios for presence-to-enum selection, findAny/findFirst Optional terminals, domain selections
with lazy fallback, side-effecting upsert boundaries, ifPresentOrElse rendering branches, and
lifecycle Optional helper boundaries. Keep them in `evals-reference/` until isolated hosted runs
classify each scenario.
