# Add string support to workflow port lookup

Use `$java-optionals` to create `WorkflowPortLookup.java` with the revised class.

Current code:

```java
import java.nio.file.Path;
import java.util.Map;
import java.util.Optional;

final class WorkflowPortLookup {
    Optional<Integer> workflowServerPortReservation(Optional<Map<String, Object>> frontMatter, Path workflowPath) {
        if (frontMatter.isEmpty()) {
            return Optional.empty();
        }
        Object value = frontMatter.get().get("server_port");
        if (value instanceof Number number) {
            return Optional.of(number.intValue());
        }
        return Optional.empty();
    }
}
```

Required changes:

- Keep support for `Number` values.
- Add support for trimmed numeric `String` values.
- Return `Optional.empty()` for absent front matter, missing values, blank strings, malformed strings, and unsupported types.
- Do not throw for malformed values.
- Do not expose `workflowPath` in output; it is included for parity with the real method.

