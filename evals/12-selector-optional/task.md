# Refactor selector Optional boundaries

Use `$java-optionals` to refactor this selector Optional code without changing behavior:

```java
import java.nio.file.Path;
import java.util.List;
import java.util.Optional;

final class DiagnosticSelector {
    Selection select(Manifest manifest, Optional<String> board, Optional<Path> workflow, Path configDir) {
        if (board.isPresent() && workflow.isPresent()) {
            throw new IllegalArgumentException("--board and --workflow cannot be used together.");
        }
        if (board.isPresent()) {
            return byBoard(manifest, board.orElseThrow());
        }
        if (workflow.isPresent()) {
            return byWorkflow(manifest, workflow.orElseThrow(), configDir);
        }
        return new Selection("none", manifest.boards(), Optional.empty());
    }

    Selection byBoard(Manifest manifest, String board) { return new Selection("board", List.of(), Optional.empty()); }
    Selection byWorkflow(Manifest manifest, Path workflow, Path configDir) { return new Selection("workflow", List.of(), Optional.of(workflow)); }
    record Manifest(List<String> boards) {}
    record Selection(String kind, List<String> boards, Optional<Path> workflow) {}
}
```
