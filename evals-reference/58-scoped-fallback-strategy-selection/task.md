# Tidy the property lookup override

Create `PropertyLookup.java` with the revised class. Assume Java 25.

Tests bind a lookup function for the duration of a block; production code reads system properties.
The override was migrated to `ScopedValue` last week and works. Tidy `get` where that makes it
clearer, keep both signatures, and keep the behavior: inside `withLookup` the given lookup answers,
outside it the system property does, a lookup that returns `null` still yields `null`, and nested
calls restore the outer lookup when the inner body finishes. Return the complete Java code only.

```java
import java.util.function.Function;
import java.util.function.Supplier;

final class PropertyLookup {
    private static final ScopedValue<Function<String, String>> LOOKUP = ScopedValue.newInstance();

    static String get(String name) {
        if (LOOKUP.isBound()) {
            Function<String, String> lookup = LOOKUP.get();
            return lookup.apply(name);
        }
        return System.getProperty(name);
    }

    static <T> T withLookup(Function<String, String> lookup, Supplier<T> body) {
        return ScopedValue.where(LOOKUP, lookup).get(body);
    }
}
```
