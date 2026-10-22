# Refactor greeting fallback

Assume Java 17.

Improve this Optional-based fallback. Create `GreetingService.java` with the revised class:

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
