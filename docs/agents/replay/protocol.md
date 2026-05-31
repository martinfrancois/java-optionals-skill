# Replay Protocol

Use this before turning a historical Optional failure into a Tessl eval.

## Inputs

For each scenario, record:

- historical starting commit;
- historical result commit, if known;
- exact user prompt to replay;
- bad-pattern oracle;
- behavior checks or tests to run.

Do not add new Optional guidance to the historical prompt. The only intended difference between
runs is skill availability.

## Worktrees

Use separate disposable worktrees:

```bash
git -C /home/server/git-projects/symphony-trello worktree add --detach \
  /tmp/java-optionals-replay/<scenario>/<variant> <starting-commit>
```

Use variants such as:

```text
without-skill
with-skill
with-skill-v2
```

## Execution

Run each prompt with a 30-minute cap:

```bash
timeout 1800s codex exec -C <worktree> --full-auto --skip-git-repo-check < <prompt-file>
```

Replay wrapper rules:

- Work only in the current checkout.
- Do not push, open PRs, publish, contact Trello, or make external state changes.
- Do not run `tessl install` or mutate agent skill folders from inside the Symphony worktree.
- Stop after local changes and local checks.
- Summarize changed files, checks, and Optional patterns intentionally left.

## Inspection

After each run, inspect the diff and scan changed Java files:

```bash
git diff --stat
git diff -- src/main/java src/test/java
rg -n "stream\\(\\)\\.toList\\(\\)|stream\\(\\)::iterator|optionalValues|presentValues|OptionalSupport|OptionalValues|CheckedOptionals|orElse\\(null\\)|\\.isPresent\\(\\)|\\.isEmpty\\(\\)|\\.orElseThrow\\(\\)|\\.get\\(\\)|getAs(Int|Long|Double)\\(" src/main/java src/test/java
```

Do not classify every match as a failure. Compare it to the scenario oracle and check whether the
value is actually reopened, null is used for local control flow, a fake one-Optional collection was
introduced, or behavior changed.

## Promotion Rule

Only add a reduced Tessl eval when:

- the full-repo without-skill replay reproduces the bad Optional pattern;
- the full-repo with-skill replay avoids it;
- behavior checks are credible; and
- the reduced eval reproduces the same difference.

If the with-skill replay still fails, first improve the skill. If the skill remains unreliable,
record the scenario as a regression target rather than claiming it as a passing eval.
