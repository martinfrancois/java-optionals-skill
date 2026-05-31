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
| B: remaining value-read cleanup | `c4e892e9e6f4889f2ad46d5529ebeb3d935dd626` | Reproduced generic checked Optional helper overreach via `OptionalSupport`. | Repeatedly failed with fake one-Optional loops or helper variants even after skill edits. | High-value regression target; concrete blocker documented. |
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

This proves the skill guidance needed stronger hard-stop wording, but it also shows a concrete
current blocker: this full-repository replay does not yet reliably obey the skill even when the
runtime guidance names the bad helper shape. Do not claim Scenario B as solved until a later
with-skill replay avoids:

- `OptionalSupport`, `OptionalValues`, `CheckedOptionals`, or equivalent checked Optional helpers;
- `OptionalBoundaries`, throwing suppliers/functions, or equivalent generic Optional helpers;
- `optional.stream().toList()` around one Optional;
- `optional.stream()::iterator`;
- `optionalValues(...)`, `presentValues(...)`, or any helper that makes one Optional iterable.

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

Because the sixth scenario is now reference-only, the active headline suite is the 5-scenario mix
from hosted run `019e7f28-31d0-73ba-b7ac-0e33e9e7023f`:

| Subset | Baseline | With context |
| --- | ---: | ---: |
| Natural activation | `258/300` | `285/300` |
| Explicit invocation | `178/200` | `200/200` |
| Combined headline | `436/500` | `485/500` |

That is a `+49/500` absolute score lift. The score ratio is about `1.11x`; the missed-point
reduction is `49/64`, or about `76.6%`.

## Checks

All completed replay commands stayed under the 30-minute cap.

Common check limitations:

- Full Maven verification in Symphony often failed because the replay sandbox blocks local
  `HttpServer` sockets with `SocketException: Operation not permitted`.
- Some runs also hit an unrelated installer assertion failure.
- Passing no-test or focused checks are recorded per run in the replay workspace logs; do not claim
  full verification passed when it was blocked by the sandbox.
