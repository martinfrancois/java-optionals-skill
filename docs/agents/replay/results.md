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
| B: remaining value-read cleanup | `c4e892e9e6f4889f2ad46d5529ebeb3d935dd626` | Reproduced generic checked Optional helper overreach via `OptionalSupport`. | Repeatedly failed with fake one-Optional loops or helper variants even after skill edits. | High-value regression target; not ready as a passing eval. |
| C: fake Optional stream/list cleanup | `8651fbbd55d70e12cf9fdb6604ace9355852697e` | Reproduced checked Optional helper overreach via `OptionalValues`. | Later with-skill run avoided helper and fake stream/list flow, using narrow checked-boundary branches. | Best current candidate for a reduced eval. |
| D: stable workflow ports | `ed2560ba0f33cea011d61e8d2c368d7020f04c42` | No distinct Optional failure found in changed production code. | Not run; lower priority after B showed remaining skill weakness. | Reference only for now. |
| E: scoped Trello handoff tools | `2880715f08299fde8ccb2b9f6925723c65b4f01c` | Broad feature implementation; one retry-after `isPresent()` / `get()` shape appeared in older package code. | Not run; scenario is broad and noisy. | Mine for smaller first-pass implementation evals. |
| F: deterministic pickup transition | `c42e36b1e3fd9a21f0a0ae494e1540e8b43a50ea` | Reproduced several value reopening patterns in broader feature code. | Not run; lower priority until narrower oracle exists. | Mine for focused cleanup evals. |

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

This proves the skill guidance needed stronger hard-stop wording, and it also proves that the
current replay case should not be claimed as solved until a later with-skill replay avoids:

- `OptionalSupport`, `OptionalValues`, `CheckedOptionals`, or equivalent checked Optional helpers;
- `optional.stream().toList()` around one Optional;
- `optional.stream()::iterator`;
- `optionalValues(...)`, `presentValues(...)`, or any helper that makes one Optional iterable.

## Checks

All completed replay commands stayed under the 30-minute cap.

Common check limitations:

- Full Maven verification in Symphony often failed because the replay sandbox blocks local
  `HttpServer` sockets with `SocketException: Operation not permitted`.
- Some runs also hit an unrelated installer assertion failure.
- Passing no-test or focused checks are recorded per run in the replay workspace logs; do not claim
  full verification passed when it was blocked by the sandbox.
