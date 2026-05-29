# Review legacy adapter

Use `$java-optionals` to review this adapter. Should this local Optional handling be changed?

```java
import java.util.Optional;

final class LegacyAdapter {
    LegacyRequest toLegacy(Optional<String> comment) {
        return new LegacyRequest(comment.orElse(null));
    }

    record LegacyRequest(String nullableComment) {}
}
```
