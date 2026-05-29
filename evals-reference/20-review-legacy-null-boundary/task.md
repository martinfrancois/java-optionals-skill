# Review legacy null boundary

Use `$java-optionals` to review this adapter. Create `review.md` with a short review decision and
rationale. Do not modify the Java code.

```java
import java.util.Optional;

final class AuditAdapter {
    AuditEvent toLegacy(Optional<String> comment) {
        return new AuditEvent(comment.orElse(null));
    }

    record AuditEvent(String nullableComment) {}
}
```
