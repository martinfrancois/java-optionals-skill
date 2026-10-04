# Preserve configured max agents during setup regeneration

You are fixing a pull request for a Trello setup connector. Assume Java 25.

Blocking finding to fix:

1. Existing workflow `agent.max_concurrent_agents` values above the setup CLI cap are promised as
   preserved but are rejected during regeneration.

Must-fix behavior: explicit CLI input and newly entered guided values remain bounded to `1..32`,
but an existing runtime-positive workflow value must be preserved when `--max-agents` is omitted
and the operator does not explicitly change it.

Current code:

import java.util.Optional;

final class TrelloSetupConnector {
    private final WorkflowConfig workflowConfig;
    private final TrelloBoardSetup boardSetup = TrelloBoardSetup.DEFAULT;

    MaxAgentsSelection selectMaxAgents(Options options, Path workflowPath) {
        if (options.maxAgentsExplicit()) {
            return new MaxAgentsSelection(options.maxAgents(), false);
        }
        Optional<Integer> configuredMaxAgents = workflowConfig.maxAgents(workflowPath);
        return new MaxAgentsSelection(
                configuredMaxAgents.orElseGet(options::maxAgents), configuredMaxAgents.isPresent());
    }

    record MaxAgentsSelection(int maxAgents, boolean fromWorkflow) {}
}

Required changes:

- Keep `MaxAgentsSelection` as the returned domain result carrying both the selected value and
  whether it came from the existing workflow configuration.
- When `--max-agents` is explicit, keep returning it with `fromWorkflow` false.
- When `--max-agents` is omitted, preserve an existing positive workflow value such as `64` even
  though it exceeds the setup input cap of `32`.
- When no workflow value exists, fall back lazily to `options.maxAgents()` without evaluating the
  fallback when a workflow value is present.
- Keep the selected value and its provenance constructed together so they cannot drift apart.
- Do not add helper types or dependencies.

Interface stubs you may assume:

interface Options {
    boolean maxAgentsExplicit();
    int maxAgents();
}

interface WorkflowConfig {
    Optional<Integer> maxAgents(Path workflowPath);
}
