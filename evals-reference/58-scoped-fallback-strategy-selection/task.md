# Replace the ThreadLocal override with a ScopedValue

Create `PropertyLookup.java`. Assume Java 25.

```java
import java.util.function.Function;

final class PropertyLookup {
    private static final ThreadLocal<Function<String, String>> LOOKUP = new ThreadLocal<>();

    static String get(String name) {
        Function<String, String> lookup = LOOKUP.get();
        return lookup == null ? System.getProperty(name) : lookup.apply(name);
    }

    static <T> T withLookup(Function<String, String> lookup, java.util.function.Supplier<T> body) {
        Function<String, String> previous = LOOKUP.get();
        LOOKUP.set(lookup);
        try {
            return body.get();
        } finally {
            if (previous == null) {
                LOOKUP.remove();
            } else {
                LOOKUP.set(previous);
            }
        }
    }
}
```

Migrate the override from `ThreadLocal` to `ScopedValue`. Keep `get` and `withLookup` with the same
signatures and the same observable behavior: inside `withLookup` the given lookup answers, outside it
the system property does, a lookup that returns `null` still yields `null`, and nested calls restore
the outer lookup when the inner body finishes. Return the complete Java code only.
