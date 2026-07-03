# Build domain selections from Optional values

Refactor `SetupSelections.java`. Assume Java 25.

Return the revised Java code only.

```java
import java.io.IOException;
import java.nio.file.Path;
import java.util.Arrays;
import java.util.Map;
import java.util.Optional;

final class SetupSelections {
    private final WorkflowConfig workflowConfig;
    private final BoardSetup boardSetup;

    SetupSelections(WorkflowConfig workflowConfig, BoardSetup boardSetup) {
        this.workflowConfig = workflowConfig;
        this.boardSetup = boardSetup;
    }

    MaxAgentsSelection configureGithubMaxAgents(Options options, Path workflowPath) {
        if (options.maxAgentsExplicit()) {
            return new MaxAgentsSelection(options.maxAgents(), false);
        }
        Optional<Integer> configuredMaxAgents = workflowConfig.maxAgents(workflowPath);
        return new MaxAgentsSelection(configuredMaxAgents.orElseGet(options::maxAgents), configuredMaxAgents.isPresent());
    }

    BoardSetup boardSetupWithCodexModel(Options options) {
        if (options.codexModelDefaults().isEmpty()) {
            return boardSetup;
        }
        CodexModelDefaults defaults = options.codexModelDefaults().orElseThrow();
        return options.hasExplicitCodexModelRequest()
                ? boardSetup.withCodexModelOverrides(defaults, options.codexModel())
                : boardSetup.withCodexModelDefaults(defaults);
    }

    public static Optional<String> firstPresent(Path dotenv, Map<String, String> environment, String... names) {
        for (String name : names) {
            String value = environment.get(name);
            if (hasText(value)) {
                return Optional.of(value);
            }
        }
        Map<String, String> dotenvValues = load(dotenv);
        for (String name : names) {
            String value = dotenvValues.get(name);
            if (hasText(value)) {
                return Optional.of(value);
            }
        }
        return Optional.empty();
    }

    int promptedMaxAgents(Terminal terminal, MaxAgentsSelection current) throws IOException {
        String answer = terminal.readLine("Maximum cards from this board at once [" + current.value() + "]: ");
        if (answer == null || answer.isBlank()) {
            return current.value();
        }
        return Integer.parseInt(answer);
    }

    private static boolean hasText(String value) {
        return value != null && !value.isBlank();
    }

    private static Map<String, String> load(Path dotenv) {
        return Map.of();
    }

    interface WorkflowConfig { Optional<Integer> maxAgents(Path workflowPath); }
    interface Options {
        boolean maxAgentsExplicit();
        int maxAgents();
        Optional<CodexModelDefaults> codexModelDefaults();
        boolean hasExplicitCodexModelRequest();
        String codexModel();
    }
    interface Terminal { String readLine(String prompt) throws IOException; }
    record MaxAgentsSelection(int value, boolean preservedFromWorkflow) {}
    record CodexModelDefaults(String model) {}
    record BoardSetup() {
        BoardSetup withCodexModelOverrides(CodexModelDefaults defaults, String model) { return this; }
        BoardSetup withCodexModelDefaults(CodexModelDefaults defaults) { return this; }
    }
}
```

Preserve explicit option precedence, workflow preservation provenance, lazy dotenv loading, and the
checked prompt boundary.
