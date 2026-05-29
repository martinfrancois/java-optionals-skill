# Refactor fake Optional collection control flow

Use `$java-optionals` to refactor this fake collection control flow:

```java
import java.util.Optional;

final class GreetingService {
    String greeting(Optional<String> name) {
        for (String value : name.stream().toList()) {
            return "Hello " + value;
        }
        return "Hello guest";
    }
}
```
