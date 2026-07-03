# Clean up enum selection

Create `BoardSetupChoices.java` with the refactored class. Improve value flow where appropriate.
Assume Java 17.

Return the complete revised Java code only.

```java
import java.util.Optional;

final class BoardSetupChoices {
    void rejectDryRunNewBoardInProgress(LocalSetupOptions options) {
        BoardSetupChoice dryRunChoice =
                options.existingBoardId().isPresent() ? BoardSetupChoice.EXISTING : BoardSetupChoice.NEW;
        rejectNewBoardInProgress(options, dryRunChoice);
    }

    BoardSetupChoice choiceWithAudit(LocalSetupOptions options, AuditLog auditLog) {
        if (options.existingBoardId().isPresent()) {
            auditLog.record("existing board selected");
            return BoardSetupChoice.EXISTING;
        }
        return BoardSetupChoice.NEW;
    }

    private void rejectNewBoardInProgress(LocalSetupOptions options, BoardSetupChoice choice) {}

    enum BoardSetupChoice {
        EXISTING,
        NEW
    }

    interface LocalSetupOptions {
        Optional<String> existingBoardId();
    }

    interface AuditLog {
        void record(String message);
    }
}
```

The present board id value is intentionally ignored in the dry-run choice. Preserve side effects and
enum values. Keep `choiceWithAudit` as an explicit imperative branch; do not hide
`auditLog.record(...)` inside an Optional `map` or other transformation callback.
