# Refactor Optional output side effects

Use `$java-optionals` to refactor this Optional output path code. Return the refactored code
followed by one sentence noting that explicit branching may be clearer if either branch throws
checked exceptions:

```java
import java.nio.file.Path;
import java.util.Optional;

final class ReportCommand {
    void finish(Optional<Path> output, String report) {
        if (output.isPresent()) {
            write(output.orElseThrow(), report);
        } else {
            print(report);
        }
    }

    void write(Path path, String report) {}
    void print(String report) {}
}
```
