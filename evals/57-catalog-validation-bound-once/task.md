# Validate reasoning effort against the model catalog

Create `ReasoningEffortChoices.java`. Assume Java 25.

Today the setup wizard validates the reasoning effort against a fixed list:

```java
import java.util.List;
import java.util.Optional;
import java.util.stream.Stream;

final class ReasoningEffortChoices {
    private static final List<String> REASONING_EFFORTS = List.of("minimal", "low", "medium", "high");

    private final ServiceCatalog catalog;

    ReasoningEffortChoices(ServiceCatalog catalog) {
        this.catalog = catalog;
    }

    List<String> reasoningChoices(String selected) {
        if (blank(selected) || REASONING_EFFORTS.contains(selected)) {
            return REASONING_EFFORTS;
        }
        return Stream.concat(Stream.of(selected), REASONING_EFFORTS.stream())
                .distinct()
                .toList();
    }

    private static boolean blank(String value) {
        return value == null || value.isBlank();
    }

    interface ServiceCatalog {
        /** The reasoning efforts the installed service advertises for a model, if it advertises any. */
        Optional<List<String>> reasoningEffortsFor(String model);
    }

    static final class SetupException extends RuntimeException {
        SetupException(String code, String message) {
            super(message);
        }
    }
}
```

Make the choices model-specific using the catalog:

- `List<String> reasoningChoices(String model, String selected)`: when the catalog advertises a list
  for the model, return exactly that list; otherwise keep today's behavior with the fixed list.
- `String validateReasoningEffort(String model, String reasoningEffort)`: when the catalog advertises
  a list for the model, return the value if it is in that list and otherwise throw
  `SetupException("setup_invalid_choice", ...)` whose message names the advertised values; when the
  model advertises no list, return the value unchanged.

Keep the class self-contained and return the complete Java code only.
