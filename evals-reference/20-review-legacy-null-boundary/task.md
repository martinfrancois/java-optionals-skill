# Review legacy null boundary

Assume Java 17.

Review this adapter. Create `review.md` with a short review decision and
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
