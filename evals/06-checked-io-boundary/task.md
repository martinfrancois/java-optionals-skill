# Refactor checked Optional prompting boundary

Use `$java-optionals` to remove Optional antipatterns from this prompting method without hiding
checked IO. Include a one-sentence rationale for the checked-IO boundary:

```java
import java.io.IOException;
import java.util.Optional;

final class WorkspaceSelector {
    String workspaceId(Options options, Terminal terminal) throws IOException {
        Optional<String> configured = options.workspaceId();
        if (configured.isPresent()) {
            return configured.get();
        }
        return promptForWorkspace(terminal);
    }

    String promptForWorkspace(Terminal terminal) throws IOException {
        return terminal.readLine("Workspace: ");
    }

    interface Options { Optional<String> workspaceId(); }
    interface Terminal { String readLine(String prompt) throws IOException; }
}
```
