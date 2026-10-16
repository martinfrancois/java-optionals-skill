# Clean up lookup rendering branch

Create `PrivateContextRenderer.java` with the refactored class. Assume Java 17.

Return the complete revised Java code only.

```java
import java.io.IOException;
import java.time.Instant;
import java.util.Optional;

final class PrivateContextRenderer {
    private String renderPrivateContext(DiagnosticsRequest request, Optional<TokenHasher> sharedTokenHasher)
            throws IOException {
        DiagnosticsContext context = diagnosticsContext(request, sharedTokenHasher);

        StringBuilder body = new StringBuilder();
        body.append("# Private Context\n\n");
        line(body, "time_utc", Instant.now().toString());
        line(body, "command", request.command());
        if (request.lookup().isPresent()) {
            section(body, "Lookup");
            appendPrivateContextLookup(body, context, request.lookup().orElseThrow());
            return body.toString();
        }

        section(body, "Local Paths");
        appendLocalPaths(body, context);
        section(body, "Workflow Identifiers");
        appendWorkflowIdentifiers(body, context);
        return body.toString();
    }

    private DiagnosticsContext diagnosticsContext(DiagnosticsRequest request, Optional<TokenHasher> hasher)
            throws IOException {
        return new DiagnosticsContext();
    }

    private static void section(StringBuilder body, String title) { body.append("\\n## ").append(title).append("\\n"); }
    private static void line(StringBuilder body, String name, String value) { body.append(name).append(": ").append(value).append("\\n"); }
    private static void appendPrivateContextLookup(StringBuilder body, DiagnosticsContext context, String lookup) {}
    private static void appendLocalPaths(StringBuilder body, DiagnosticsContext context) {}
    private static void appendWorkflowIdentifiers(StringBuilder body, DiagnosticsContext context) {}

    record DiagnosticsRequest(String command, Optional<String> lookup) {}
    record DiagnosticsContext() {}
    record TokenHasher() {}
}
```

When lookup is present, render only the lookup section after the common header. When lookup is absent,
render the full private context sections. Preserve ordering and checked exception behavior.
Use `ifPresentOrElse` or an equivalent Optional terminal for the side-effecting present and absent
branches; do not hide rendering mutations inside `map` or another fake transformation.
