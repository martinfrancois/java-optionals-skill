# Refactor order-independent findFirst

Use `$java-optionals` to refactor this order-independent lookup. Return the refactored code followed
by one sentence explaining why `findAny` is appropriate:

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
