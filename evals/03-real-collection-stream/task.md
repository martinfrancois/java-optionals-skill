# Review command option lookup

Use `$java-optionals` to review this lookup. Should the Optional usage be changed? Answer with a
short review comment even if no code change is needed.

```java
import java.util.Optional;
import java.util.Set;

final class CommandRedactor {
    private static final Set<String> SECRET_OPTIONS = Set.of("--token", "--api-key");

    Optional<String> secretOption(String arg) {
        return SECRET_OPTIONS.stream()
                .filter(option -> arg.equals(option) || arg.startsWith(option + "="))
                .findAny();
    }
}
```
