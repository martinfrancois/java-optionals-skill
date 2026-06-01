# Historical Replay Results

Replay workspace:

```text
/tmp/java-optionals-replay-20260531-165239
```

These results are local replay evidence, not hosted Tessl benchmark results.

## Current Classification

| Scenario | Starting commit | Without skill | With skill | Classification |
| --- | --- | --- | --- | --- |
| A: `.orElse(null)` cleanup follow-up | `e5e1dfc171dc679cc9e0e752d69fb8337ef20c81` | Reproduced internal `orElse(null)` cleanup risk while also fixing the main workpad branch. | Initial with-skill run was broad and still introduced fake one-Optional stream/list flow. | Useful history, but too broad until narrowed. |
| B: remaining value-read cleanup | `c4e892e9e6f4889f2ad46d5529ebeb3d935dd626` | Reproduced generic checked Optional helper overreach via `OptionalSupport`. | Valid v10 replay avoided fake helper/list moves and passed full verification after formatting. | Reduced into headline eval 11. |
| C: fake Optional stream/list cleanup | `8651fbbd55d70e12cf9fdb6604ace9355852697e` | Reproduced checked Optional helper overreach via `OptionalValues`. | Later with-skill run avoided helper and fake stream/list flow, using narrow checked-boundary branches. | Full-repo evidence is strong; reduced reference eval is not headline-faithful yet. |
| D: stable workflow ports | `ed2560ba0f33cea011d61e8d2c368d7020f04c42` | No distinct Optional failure found in changed production code. | Also no distinct Optional failure found. | Reference only. |
| E: scoped Trello handoff tools | `2880715f08299fde8ccb2b9f6925723c65b4f01c` | Broad feature implementation; one retry-after `isPresent()` / `get()` shape appeared in older package code. | Broad feature implementation without a focused Optional cleanup oracle. | Reference only / mine for smaller first-pass implementation evals. |
| F: deterministic pickup transition | `c42e36b1e3fd9a21f0a0ae494e1540e8b43a50ea` | Reproduced several value reopening patterns in broader feature code. | Changed the requested pickup flow, but left unrelated pre-existing Optional value reopening in touched files. | Reference only / mine for focused cleanup evals. |

## Scenario B Iterations

Scenario B is the clearest live finding from this replay cycle.

Without skill, the agent introduced checked Optional helper abstraction:

```text
OptionalSupport.orElseGet(...)
OptionalSupport.map(frontMatter, value -> yaml.readValue(value, MAP_TYPE))
```

With skill attempts:

| Variant | Result |
| --- | --- |
| `with-skill-v2` | Replaced helpers with `optionalValues(Optional<T>)` and `optional.stream()::iterator`. |
| `with-skill-v3` | Replaced helpers with `for (... : optional.stream().toList())` loops. |
| `with-skill-v4` | Still used `for (... : optional.stream().toList())` loops. |
| `with-skill-v5` | Renamed the disguised helper to `presentValues(Optional<T>)`, still backed by `optional.stream()::iterator`. |
| `with-skill-v6` | Still used `for (... : optional.stream().toList())` loops and attempted checked parsing cleanup through Optional flow. |
| `with-skill-v7` | Introduced `OptionalBoundaries` with throwing suppliers/functions and `optional.stream().iterator()`, despite the skill banning generic Optional helpers. |
| `with-skill-v8` | Invalid replay: sandbox prevented the agent from reading the installed skill. |
| `with-skill-v9` | Invalid replay: adding `/root/.tessl` as a writable dir broke sandbox setup before edits. |
| `with-skill-v10` | Valid replay: used `--sandbox danger-full-access`, read the installed skill, avoided fake helpers/iterables, and passed `./mvnw -q spotless:check verify` after formatting. |

This proved the skill guidance needed two additions:

- `OptionalSupport`, `OptionalValues`, `CheckedOptionals`, or equivalent checked Optional helpers;
- `OptionalBoundaries`, throwing suppliers/functions, or equivalent generic Optional helpers;
- `optional.stream().toList()` around one Optional;
- `optional.stream()::iterator`;
- `optionalValues(...)`, `presentValues(...)`, or any helper that makes one Optional iterable.

It also proved the replay harness needs enough filesystem access for Codex to read installed
skills. Runs where the agent says it will use the skill but cannot read the skill body are not valid
with-skill evidence.

## Scenario B Reduction

Scenario B was reduced into:

```text
evals/11-checked-boundary-selection-cleanup
```

The reduced scenario keeps the historically important shape:

- `isPresent()` / `orElseThrow()` and `isEmpty()` / `orElseThrow()` cleanup requests;
- checked prompt fallback;
- checked YAML parsing;
- ordinary requested-port fallback where `map(...).orElseGet(...)` is appropriate;
- criteria that reject generic checked Optional helpers, fake one-Optional iterables, and local
  null-control-flow workarounds.

Hosted run:

```text
019e7f40-b788-74b8-97c8-e03bf6aa8190
```

The reduced baseline scored `80/100`: it preserved behavior but lost the ordinary Optional-boundary
and replacement-antipattern criteria. With context scored `100/100`. This matches the full-repo
finding closely enough to keep the scenario in the headline suite.

## Scenario C Reduction

Scenario C was reduced into:

```text
evals-reference/47-checked-boundary-fake-optional-list-cleanup
```

The reduced scenario keeps the historically important shape:

- fake `Optional.stream().toList()` loops over one Optional;
- checked prompt fallback;
- checked YAML parsing;
- ordinary requested-port fallback where `map(...).orElseGet(...)` is appropriate;
- criteria that reject fake Optional iterables, generic checked Optional helpers, and checked
  exception tunneling.

Hosted checks showed the reduced scenario is useful as reference material, but not yet faithful
enough for the headline suite:

```text
019e7f0f-2153-728d-8949-57f22ffc22da
019e7f1e-9d83-740b-a731-b09dc52a1738
019e7f22-526a-7529-942b-64d50e8db82d
```

In the latest run, the reduced baseline scored `95/100` on this scenario and received full credit
for avoiding fake Optional collections and helpers. That means it did not reproduce the full-repo
failure where the baseline introduced `OptionalValues`. Keep it out of headline evals until a
smaller fixture reproduces that same without-skill vs with-skill difference.

The latest 6-scenario temporary headline run was:

| Subset | Baseline | With context |
| --- | ---: | ---: |
| Natural activation | `353/400` | `385/400` |
| Explicit invocation | `178/200` | `200/200` |
| Combined temporary suite | `531/600` | `585/600` |

Because the reduced Scenario B case is now headline-active, the completed pre-reweight headline run
is the 6-scenario mix from hosted run `019e7f40-b788-74b8-97c8-e03bf6aa8190`:

| Subset | Baseline | With context |
| --- | ---: | ---: |
| Natural activation | `338/400` | `400/400` |
| Explicit invocation | `178/200` | `200/200` |
| Combined headline | `516/600` | `600/600` |

That is a `+84/600` absolute score lift. The score ratio is about `1.16x`; the missed-point
reduction is `84/84`, or `100%`.

Category subtotal:

| Category | Baseline | With context |
| --- | ---: | ---: |
| Safety gates | `395/395` | `395/395` |
| Optional quality | `98/180` | `180/180` |
| Maintainability | `23/25` | `25/25` |

The Optional-quality subtotal is the clearest skill-specific number: `+82/180`, about `1.84x` by
raw score ratio, with `100%` missed-point reduction. Safety gates stay in the benchmark to prevent
broken code from scoring well, but they should not be treated as the main value claim.

After commit `4c7fb58`, headline criteria were reweighted to make each 100-point scenario score
`35` safety, `60` Optional quality, and `5` maintainability. Across the six-scenario headline suite,
that is `210` safety points, `360` Optional-quality points, and `30` maintainability points. Hosted
run `019e80aa-4b2b-75af-9ce3-502c45d76c4e` was started against the dirty pre-commit working tree
with those weights, but one baseline score was still pending when checked. Do not use that run as a
final release claim until it finishes or is rerun from a clean commit.

The current focused headline suite keeps only direct evidence for the plugin summary: helping AI
coding agents use Java Optional well in new code and cleanups without replacing one antipattern with
another. Baseline-solved and less central scenarios remain in `evals-reference/`. Hosted run
`019e811b-e9da-71fb-adf6-74fb3265a68d` was run from clean commit `917a32e`:

| Subset | Baseline | With context |
| --- | ---: | ---: |
| Natural activation | `90/200` | `200/200` |
| Explicit invocation | `56/100` | `98/100` |
| Combined headline | `146/300` | `298/300` |

That is a `+152/300` absolute score lift. The raw score ratio is `2.04x`; missed-point reduction is
`152/154`, or `98.7%`.

Category subtotal:

| Category | Baseline | With context |
| --- | ---: | ---: |
| Safety gates | `75/75` | `75/75` |
| Optional quality | `56/210` | `208/210` |
| Maintainability | `15/15` | `15/15` |

The Optional-quality subtotal is `3.71x` by raw score ratio. The headline result should be read
with the reference suite: moved scenarios still matter as regression coverage, but they're not the
best public evidence for this plugin's stated purpose.

## Checks

All completed replay commands stayed under the 30-minute cap.

Common check limitations:

- Full Maven verification in Symphony often failed because the replay sandbox blocks local
  `HttpServer` sockets with `SocketException: Operation not permitted`.
- Some runs also hit an unrelated installer assertion failure.
- Passing no-test or focused checks are recorded per run in the replay workspace logs; do not claim
  full verification passed when it was blocked by the sandbox.
