# Refactor required config lookup

Assume Java 17.

Improve this lookup without changing its error behavior:

```java
import java.util.Map;
import java.util.Optional;

final class ConfigLookup {
    String required(Map<String, String> values, String key) {
        Optional<String> value = Optional.ofNullable(values.get(key));
        if (value.isPresent()) {
            return value.get();
        }
        throw new IllegalArgumentException("Missing config: " + key);
    }
}
```
