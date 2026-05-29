# Review proposed Vavr local overreach

Use `$java-optionals` to review this proposed cleanup. Create `review.md` with a short review
decision and rationale.

Before:

```java
import java.io.IOException;
import java.util.Optional;

final class WorkspaceSelector {
    String workspaceId(Options options, Terminal terminal) throws IOException {
        Optional<String> configured = options.workspaceId();
        if (configured.isEmpty()) {
            return promptForWorkspace(terminal);
        }
        return configured.orElseThrow();
    }

    String promptForWorkspace(Terminal terminal) throws IOException {
        return terminal.readLine("Workspace: ");
    }

    interface Options { Optional<String> workspaceId(); }
    interface Terminal { String readLine(String prompt) throws IOException; }
}
```

Proposed:

```java
import io.vavr.control.Option;
import java.io.IOException;
import java.util.Optional;

final class WorkspaceSelector {
    String workspaceId(Options options, Terminal terminal) throws IOException {
        return Option.ofOptional(options.workspaceId())
                .getOrElseTry(() -> promptForWorkspace(terminal));
    }

    String promptForWorkspace(Terminal terminal) throws IOException {
        return terminal.readLine("Workspace: ");
    }

    interface Options { Optional<String> workspaceId(); }
    interface Terminal { String readLine(String prompt) throws IOException; }
}
```

