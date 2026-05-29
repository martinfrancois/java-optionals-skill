# Refactor order-independent findFirst

Use `$java-optionals` to refactor this order-independent lookup and include a one-sentence
rationale:

```java
import java.util.Optional;
import java.util.Set;

final class FlagMatcher {
    Optional<String> matchingFlag(Set<String> flags, String arg) {
        return flags.stream()
                .filter(flag -> arg.equals(flag) || arg.startsWith(flag + "="))
                .findFirst();
    }
}
```
