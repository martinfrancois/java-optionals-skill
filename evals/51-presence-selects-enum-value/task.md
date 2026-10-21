# Clean up enum selection

Create `BoardSetupChoices.java` with the revised class. Assume Java 17. Tidy the value flow where it
helps without changing behavior, and return the complete revised Java code only.

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

Keep the audit record call and when it happens.
