# Add a lookup mode to the private context renderer

Create `PrivateContextRenderer.java` with the revised class. Assume Java 17. Add lookup support to
`renderPrivateContext`: `DiagnosticsRequest` now carries `Optional<String> lookup()`. When a lookup is
present, render the common header and then only a `Lookup` section built with
`appendPrivateContextLookup(body, context, lookup)`. When it is absent, render the full private context
as today. Keep the header order and the checked `IOException`. Return the complete revised Java code
only.

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

    private static void section(StringBuilder body, String title) { body.append("\n## ").append(title).append("\n"); }
    private static void line(StringBuilder body, String name, String value) { body.append(name).append(": ").append(value).append("\n"); }
    private static void appendPrivateContextLookup(StringBuilder body, DiagnosticsContext context, String lookup) {}
    private static void appendLocalPaths(StringBuilder body, DiagnosticsContext context) {}
    private static void appendWorkflowIdentifiers(StringBuilder body, DiagnosticsContext context) {}

    record DiagnosticsRequest(String command, Optional<String> lookup) {}
    record DiagnosticsContext() {}
    record TokenHasher() {}
}
```
