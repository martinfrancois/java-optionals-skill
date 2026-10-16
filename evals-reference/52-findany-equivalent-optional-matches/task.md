# Audit Optional stream lookup terminals

Refactor `OptionalLookupTerminals.java` only where the terminal operation better communicates the
contract. Assume Java 17.

Return the revised Java code and one brief comment beside each retained `findFirst()` explaining why
the first match is semantically required.

```java
import java.nio.file.Path;
import java.util.List;
import java.util.Locale;
import java.util.Optional;

final class OptionalLookupTerminals {
    static Optional<String> detectedList(List<String> openListNames, String expectedName) {
        return openListNames.stream()
                .filter(name -> name.equalsIgnoreCase(expectedName))
                .findFirst();
    }

    static Optional<BoardList> targetList(List<BoardList> lists, String configuredName) {
        String expected = normalize(configuredName);
        return lists.stream()
                .filter(list -> !list.closed())
                .filter(list -> normalize(list.name()).equals(expected))
                .findFirst();
    }

    static Optional<Path> firstExecutable(List<Path> searchPath, String commandName) {
        return searchPath.stream()
                .map(path -> path.resolve(commandName))
                .filter(path -> path.toFile().exists())
                .findFirst();
    }

    static Optional<Integer> firstJavaMajor(String output) {
        return output.lines()
                .map(String::stripLeading)
                .filter(line -> line.startsWith("java "))
                .map(OptionalLookupTerminals::firstInteger)
                .flatMap(Optional::stream)
                .findFirst();
    }

    private static Optional<Integer> firstInteger(String value) {
        return Optional.empty();
    }

    private static String normalize(String value) {
        return value.toLowerCase(Locale.ROOT).replaceAll("\\s+", " ").strip();
    }

    record BoardList(String id, String name, boolean closed) {}
}
```
