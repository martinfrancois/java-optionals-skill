# Refactor lifecycle selector validation

Refactor this lifecycle selector validation so status, stop, and logs share the same explicit
workflow preflight before loading the manifest. Preserve behavior and public messages. Keep the
change small. Assume Java 17.

Create `LocalWorkerManager.java` with the revised class. Return the complete revised Java code only.
The shared preflight should bind `workflow` at the Optional boundary and call a Path-taking
validation helper; do not keep `Optional.isEmpty()` followed by `Optional.get()` inside the helper.
Do not leave `requireExistingExplicitWorkflow(Optional<Path> workflow)` in place; after the refactor,
the selected workflow validation helper should receive a `Path`, and the code should not call
`workflow.get()`.
Do not duplicate the `workflow.map(...).ifPresent(...)` preflight chain in `stop`, `status`, and
`logs`; extract that Optional-boundary preflight into one shared helper called by all three methods.

```java
import java.io.IOException;
import java.io.PrintStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.Optional;

final class LocalWorkerManager {
    int stop(StopWorkerRequest request, PrintStream out) throws IOException {
        LocalWorkerPaths paths = LocalWorkerPaths.from(request.configDir());
        requireExistingExplicitWorkflow(request.workflow());
        ConnectedBoardManifest manifest = new ConnectedBoardRepository(paths.manifestPath()).loadForLifecycle();
        List<ConnectedBoard> boards = selectForStop(manifest, request.board(), request.workflow());
        return boards.size();
    }

    int status(WorkerStatusRequest request, PrintStream out) throws IOException {
        LocalWorkerPaths paths = LocalWorkerPaths.from(request.configDir());
        requireExistingExplicitWorkflow(request.workflow());
        ConnectedBoardManifest manifest = new ConnectedBoardRepository(paths.manifestPath()).loadForLifecycle();
        List<ConnectedBoard> boards = selectForStatus(manifest, request.board(), request.workflow());
        return boards.size();
    }

    int logs(WorkerLogsRequest request, PrintStream out) throws IOException {
        LocalWorkerPaths paths = LocalWorkerPaths.from(request.configDir());
        requireExistingExplicitWorkflow(request.workflow());
        ConnectedBoardManifest manifest = new ConnectedBoardRepository(paths.manifestPath()).loadForLifecycle();
        ConnectedBoard board = selectOne(manifest, request.board(), request.workflow());
        return board.name().length();
    }

    private static void requireExistingExplicitWorkflow(Optional<Path> workflow) {
        if (workflow.isEmpty()) {
            return;
        }
        Path workflowPath = workflow.get().toAbsolutePath().normalize();
        if (!Files.exists(workflowPath)) {
            throw new TrelloBoardSetupException(
                    "setup_invalid_arguments", "--workflow must point to an existing workflow file.");
        }
        validateWorkerWorkflowPath(workflowPath);
    }

    private static void validateWorkerWorkflowPath(Path workflowPath) {
        if (Files.exists(workflowPath) && !Files.isRegularFile(workflowPath)) {
            throw new TrelloBoardSetupException(
                    "setup_invalid_arguments", "--workflow must point to a regular workflow file.");
        }
    }

    private List<ConnectedBoard> selectForStop(
            ConnectedBoardManifest manifest, Optional<String> board, Optional<Path> workflow) {
        return List.of();
    }

    private List<ConnectedBoard> selectForStatus(
            ConnectedBoardManifest manifest, Optional<String> board, Optional<Path> workflow) {
        return List.of();
    }

    private ConnectedBoard selectOne(ConnectedBoardManifest manifest, Optional<String> board, Optional<Path> workflow) {
        return new ConnectedBoard("demo");
    }

    record StopWorkerRequest(Path configDir, Optional<String> board, Optional<Path> workflow) {}
    record WorkerStatusRequest(Path configDir, Optional<String> board, Optional<Path> workflow) {}
    record WorkerLogsRequest(Path configDir, Optional<String> board, Optional<Path> workflow) {}
    record LocalWorkerPaths(Path manifestPath) {
        static LocalWorkerPaths from(Path configDir) {
            return new LocalWorkerPaths(configDir.resolve("connected-boards.json"));
        }
    }
    record ConnectedBoard(String name) {}
    record ConnectedBoardManifest(List<ConnectedBoard> boards) {}
    static final class ConnectedBoardRepository {
        ConnectedBoardRepository(Path manifestPath) {}
        ConnectedBoardManifest loadForLifecycle() throws IOException {
            return new ConnectedBoardManifest(List.of());
        }
    }
    static final class TrelloBoardSetupException extends RuntimeException {
        TrelloBoardSetupException(String code, String message) {
            super(message);
        }
    }
}
```
