# Refactor report output

Use `$java-optionals` to improve this output handling and include a concise rationale:

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
